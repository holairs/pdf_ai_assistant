from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from process_data import process_pdfs 
from utils.generate_pdf import generate_pdf_from_db
from db_config import get_db
import asyncpg

app = FastAPI()
DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'
# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/request_employee")
async def request_employee(request: Request):
    print("📡 Recibida petición en /request_employee")
    try:
        body = await request.json()
        print("📜 Cuerpo recibido:", body)

        prompt = body.get("prompt")  # Get prompt from JSON

        if not prompt:
            print("⚠️ Error: No se proporcionó un prompt")
            return JSONResponse(content={"error": "Falta el prompt"}, status_code=400)

        print("🎯 Procesando PDFs con el prompt:", prompt)
        result = await process_pdfs(prompt)
        print("✅ Respuesta generada:", result)
        return JSONResponse(content=result)

    except Exception as e:
        print(f"❌ Error interno en FastAPI: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/history")
async def get_history():
    """Devuelve el historial de conversaciones guardadas en PostgreSQL."""
    conn = await asyncpg.connect(DATABASE_URL)
    conversations = await conn.fetch("SELECT id, prompt, created_at, title, profile FROM conversations ORDER BY created_at DESC")
    await conn.close()

    return [{"id": conv["id"], "prompt": conv["prompt"], "created_at": conv["created_at"], "title": conv["title"], "profile": conv["profile"]} for conv in conversations]

@app.get("/get_processed_profiles/{conversation_id}")
async def get_processed_profiles(conversation_id: int):
    """Devuelve los candidatos asociados a una conversación."""
    conn = await asyncpg.connect(DATABASE_URL)
    processed_profiles = await conn.fetch(
        "SELECT candidate_name FROM pdf_files WHERE conversation_id = $1",
        conversation_id
    )
    await conn.close()

    return [{"candidateName": conv["candidate_name"]} for conv in processed_profiles]

@app.get("/download/{conversation_id}/{candidate_name}")
async def download_pdf(conversation_id: int, candidate_name: str):
    """Genera un PDF desde la BD y lo devuelve como archivo descargable."""
    try:
        pdf_bytes = await generate_pdf_from_db(conversation_id, candidate_name)
        if not pdf_bytes:
            raise HTTPException(status_code=404, detail="No se encontró el archivo PDF.")

        return Response(content=pdf_bytes, media_type="application/pdf",
                        headers={"Content-Disposition": f"attachment; filename={candidate_name}.pdf"})
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))
