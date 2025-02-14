from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from extraction import process_pdfs 

app = FastAPI()

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
