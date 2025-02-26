import os
import asyncpg
import re
from PyPDF2 import PdfReader
from agents.hr_agent import hr_analysis
from agents.tec_agent import tec_analysis
from agents.qa_agent import qa_analysis
from open_ai import ai_consult

DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'
PDF_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/CVS_Test/")

async def extract_tags(text: str):
    """Extrae datos de los tags en la respuesta de OpenAI."""
    title_match = re.search(r"<TITLE>(.*?)</TITLE>", text, re.DOTALL)
    profile_match = re.search(r"<PROFILE>(.*?)</PROFILE>", text, re.DOTALL)
    content_match = re.findall(r"<PERSON>(.*?)</PERSON>", text, re.DOTALL)  # Lista de candidatos

    title = title_match.group(1).strip() if title_match else "Sin título"
    profile = profile_match.group(1).strip() if profile_match else "Sin perfil"
    persons = [p.strip() for p in content_match] if content_match else []

    return title, profile, persons

def extract_candidate_name(person_text: str):
    """Extrae el nombre del candidato de la sección <PERSON>."""
    # Intentar con el formato: **Nombre:** Nombre Apellido
    name_match = re.search(r"\*\*Nombre:\*\* (.*?)\n", person_text)
    
    if name_match:
        return name_match.group(1).strip()

    # Si no se encontró con "Nombre:", buscar el primer texto en negrita (**Texto**)
    bold_match = re.search(r"\*\*(.*?)\*\*", person_text)
    
    if bold_match:
        return bold_match.group(1).strip()

    return "Desconocido"  # Si no se encuentra nada, usar "Desconocido"

def extract_candidate_calification(person_text: str):
    """Extrae el nombre del candidato de la sección <PERSON>."""
    # Intentar con el formato: **Nombre:** Nombre Apellido
    calification_match = re.search(r"\*\*Calificación:\*\* (.*?)\n", person_text)
    
    if calification_match:
        return calification_match.group(1).strip()

    # Si no se encontró con "Nombre:", buscar el primer texto en negrita (**Texto**)
    bold_match = re.search(r"\*\*(.*?)\*\*", person_text)
    
    if bold_match:
        return bold_match.group(1).strip()

    return "Desconocido"  # Si no se encuentra nada, usar "Desconocido"

async def save_conversation(prompt: str, title: str, profile: str):
    """Guarda la conversación en la base de datos y devuelve su ID."""
    conn = await asyncpg.connect(DATABASE_URL)
    conversation_id = await conn.fetchval(
        "INSERT INTO conversations (prompt, title, profile) VALUES ($1, $2, $3) RETURNING id",
        prompt, title, profile
    )
    await conn.close()
    return conversation_id

async def save_pdf(conversation_id: int, candidate_name: str, markdown_content: str):
    """Guarda el markdown de un candidato en la base de datos."""
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO pdf_files (conversation_id, candidate_name, markdown_content) VALUES ($1, $2, $3)",
        conversation_id, candidate_name, markdown_content
    )
    await conn.close()

async def process_pdfs(prompt: str):
    """Procesa PDFs, obtiene respuesta de OpenAI y almacena los datos."""
    pdf_data = {}
    open_ai_response = "Error: No se pudo procesar ningún PDF"
    candidates_list = []

    try:
        # Leer los PDFs en la carpeta
        for filename in os.listdir(PDF_FOLDER):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(PDF_FOLDER, filename)
                try:
                    with open(pdf_path, "rb") as pdf_file:
                        reader = PdfReader(pdf_file)
                        text = "\n".join([page.extract_text() or "" for page in reader.pages])
                        pdf_data[filename] = text
                except Exception as e:
                    print(f"❌ Error procesando {filename}: {e}")

        if pdf_data:
            # Obtener respuesta de OpenAI
            formatted_data = {"prompt": prompt, "pdfs": pdf_data}
            open_ai_response = ai_consult(formatted_data)

            # Extraer información de los tags en la respuesta
            title, profile, persons = await extract_tags(open_ai_response)

            # Guardar conversación en la base de datos
            conversation_id = await save_conversation(prompt, title, profile)

            # Guardar cada persona en la tabla `pdf_files`
            for person in persons:
                candidate_name = extract_candidate_name(person)
                candidate_calification = extract_candidate_calification(person)
                await save_pdf(conversation_id, candidate_name, person)

                hr_feedback = hr_analysis(person)  # Obtener análisis de RRHH
                tec_feedback = tec_analysis(person)  # Obtener análisis técnico
                qa_feedback = qa_analysis(person)  # Obtener análisis de QA

                print(f"👥 {candidate_name}: {hr_feedback}")

                # Añadir a la lista de candidatos para el UI
                candidates_list.append({
                    "name": candidate_name,
                    "calification": candidate_calification, 
                    "hr_feedback": hr_feedback,
                    "conversationId": conversation_id
                    })

            return {
                "conversationId": conversation_id,
                "title": title,
                "profile": profile,
                "candidates": candidates_list,  # Agregamos la lista de candidatos aquí
            }

        else:
            print("⚠️ No hay suficientes archivos para procesar.")
            return {"error": "No hay archivos PDF válidos en la carpeta."}

    except Exception as e:
        print(f"❌ Error en FastAPI: {e}")
        return {"error": str(e)}
