# extraction.py

from io import BytesIO
from PyPDF2 import PdfReader

from open_ai import ai_consult

async def get_pdf_data(file):
    try:
        contents = await file.read()
        pdf_file = BytesIO(contents)
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error while processing the PDF: {e}")
        return None

async def upload_files(files):
    pdf_data: Dict[str, str] = {}

    for file in files:
        text = await get_pdf_data(file)
        if text:
            pdf_data[file.filename] = text
        else:
            pdf_data[file.filename] = "Error while processing the PDF"

    open_ai_response = ai_consult(str(pdf_data))
    return {"ai_response": open_ai_response}
