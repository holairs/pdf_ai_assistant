import os
import asyncpg
import re
from PyPDF2 import PdfReader
from fpdf import FPDF
from open_ai import ai_consult

DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'

async def save_conversation(prompt: str, response_markdown: str):
    """Guarda la conversación en la base de datos y devuelve el ID."""
    conn = await asyncpg.connect(DATABASE_URL)
    conversation_id = await conn.fetchval(
        "INSERT INTO conversations (prompt, response_markdown) VALUES ($1, $2) RETURNING id",
        prompt, response_markdown
    )
    await conn.close()
    return conversation_id

async def save_pdf(conversation_id: int, candidate_name: str, pdf_bytes: bytes):
    """Guarda el PDF generado en la base de datos."""
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        "INSERT INTO pdf_files (conversation_id, candidate_name, pdf_data) VALUES ($1, $2, $3)",
        conversation_id, candidate_name, pdf_bytes
    )
    await conn.close()

def markdown_to_pdfs(markdown_text: str):
    """Convierte el Markdown en PDFs y devuelve los binarios."""
    pdf_files = {}

    candidate_sections = re.split(r"##\s+", markdown_text)  # Separar candidatos por título ##

    for section in candidate_sections:
        if not section.strip():
            continue

        lines = section.split("\n")
        candidate_name = lines[0].strip().replace(" ", "_")
        content = "\n".join(lines[1:])

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(190, 10, content)

        pdf_bytes = pdf.output(dest="S").encode("latin1")  # Obtener PDF en bytes
        pdf_files[candidate_name] = pdf_bytes

    return pdf_files

async def process_pdfs(prompt: str):
    """Procesa los PDFs, almacena la respuesta y los PDFs en PostgreSQL."""
    pdf_data = {}
    open_ai_response = "Error: No se pudo procesar ningún PDF"

    try:
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
            formatted_data = {"prompt": prompt, "pdfs": pdf_data}
            open_ai_response = ai_consult(formatted_data)

            # Guardar la conversación en la base de datos
            conversation_id = await save_conversation(prompt, open_ai_response)

            # Convertir Markdown en PDFs y almacenarlos
            pdf_files = markdown_to_pdfs(open_ai_response)
            for candidate_name, pdf_bytes in pdf_files.items():
                await save_pdf(conversation_id, candidate_name, pdf_bytes)

            return {
                "conversation_id": conversation_id,
                "ai_response": f"```markdown\n{open_ai_response}\n```"
            }

        else:
            print("⚠️ No hay suficientes archivos para procesar.")
            return {"error": "No hay archivos PDF válidos en la carpeta."}

    except Exception as e:
        print(f"❌ Error en FastAPI: {e}")
        return {"error": str(e)}
