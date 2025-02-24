from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from process_data import process_pdfs 
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
    conversations = await conn.fetch("SELECT id, prompt, created_at FROM conversations ORDER BY created_at DESC")
    await conn.close()

    return [{"id": conv["id"], "prompt": conv["prompt"], "created_at": conv["created_at"]} for conv in conversations]


@app.get("/download/{conversation_id}/{candidate_name}")
async def download_pdf(conversation_id: int, candidate_name: str):
    """Devuelve el PDF de un candidato almacenado en PostgreSQL."""
    conn = await asyncpg.connect(DATABASE_URL)
    pdf_data = await conn.fetchval(
        "SELECT pdf_data FROM pdf_files WHERE conversation_id = $1 AND candidate_name = $2",
        conversation_id, candidate_name
    )
    await conn.close()

    if pdf_data:
        return Response(content=pdf_data, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={candidate_name}.pdf"})
    return JSONResponse(content={"error": "Archivo no encontrado"}, status_code=404)

