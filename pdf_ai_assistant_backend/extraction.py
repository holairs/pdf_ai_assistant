import os
from PyPDF2 import PdfReader
from open_ai import ai_consult

PDF_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads/CVS_Test/")

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
        else:
            print("⚠️ Not enough files to process.")

    except Exception as e:
        print(f"❌ Error in FastAPI: {e}")

    return {"ai_response": open_ai_response}
