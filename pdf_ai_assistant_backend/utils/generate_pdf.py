import asyncpg
import markdown2
from weasyprint import HTML 
import os

DATABASE_URL = 'postgresql://holairs:Panic!@localhost:5432/ai_assistant'

async def get_markdown_from_db(conversation_id: int, candidate_name: str):
    """Obtiene el contenido en Markdown desde la base de datos."""
    conn = await asyncpg.connect(DATABASE_URL)
    result = await conn.fetchrow(
        "SELECT markdown_content FROM pdf_files WHERE conversation_id = $1 AND candidate_name = $2",
        conversation_id, candidate_name
    )
    await conn.close()
    return result["markdown_content"] if result else None

def markdown_to_pdf(candidate_name: str, markdown_content: str):
    """Convierte Markdown a HTML y luego a PDF con diseño de CV."""
    
    # ** Verificar la Ruta del Logo **
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    logo_url = f"file://{os.path.join(BASE_DIR, 'assets', 'ey_logo.png')}"  

    # ** Plantilla HTML con estilos **
    html_template = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 18px; /* 🔹 Tamaño de fuente más grande */
                margin: 40px;
                padding: 0;
            }}
            .header {{
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                border-bottom: 3px solid #333;
                padding-bottom: 5px;
                margin-bottom: 30px;
            }}
            .logo {{
                width: 140px;
                height: auto;
            }}
            .name {{
                font-size: 28px;
                font-weight: bold;
                color: #333;
                margin-bottom: 0;
            }}
            .section-title {{
                font-size: 22px;
                font-weight: bold;
                color: #007BFF;
                margin-top: 20px;
                border-bottom: 2px solid #007BFF;
                padding-bottom: 5px;
            }}
            ul {{
                padding-left: 30px;
                list-style-type: disc !important; /* 🔹 Fuerza los bullets como círculos */
            }}
            li {{
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img class="logo" src="{logo_url}" alt="Logo">
            <div class="name">{candidate_name}</div>
        </div>
        {markdown2.markdown(markdown_content)}
    </body>
    </html>
    """

    # ** Convertir HTML a PDF **
    pdf = HTML(string=html_template).write_pdf()
    return pdf

async def generate_pdf_from_db(conversation_id: int, candidate_name: str):
    """Genera un PDF con formato de CV en memoria desde la BD y lo devuelve en binario."""
    markdown_content = await get_markdown_from_db(conversation_id, candidate_name)
    if not markdown_content:
        return None
    return markdown_to_pdf(candidate_name, markdown_content)
