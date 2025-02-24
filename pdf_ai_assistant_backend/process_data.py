import os
import asyncpg
import re
from PyPDF2 import PdfReader
from fpdf import FPDF
from open_ai import ai_consult

DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'
# PDF_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/CVS_Test/")
PDF_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/CVS_Test_minimal/")

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
    pdf_data = {}
    open_ai_response = "Error: No se pudo procesar ningún PDF"  # Defatult value

    try:
        # List directory PDFs 
        for filename in os.listdir(PDF_FOLDER):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(PDF_FOLDER, filename)
                try:
                    with open(pdf_path, "rb") as pdf_file:
                        reader = PdfReader(pdf_file)
                        text = "\n".join([page.extract_text() or "" for page in reader.pages])

                        # Contents as str
                        if not isinstance(text, str):
                            raise ValueError(f"The {filename} content is not a valid str.")

                        pdf_data[filename] = text
                except Exception as e:
                    print(f"❌ Error while processing {filename}: {e}")

        if pdf_data:
            formatted_data = {
                "prompt": prompt,
                "pdfs": pdf_data
            }
            open_ai_response = ai_consult(formatted_data)  # Formated values
            save_pdf(1, "Test", open_ai_response.encode("utf-8"))
        else:
            print("⚠️ Not enough files to process.")

    except Exception as e:
        print(f"❌ Error in FastAPI: {e}")

    return {"ai_response": open_ai_response}
