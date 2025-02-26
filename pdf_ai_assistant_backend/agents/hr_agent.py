# project/agents/hr_agent.py

from openai import OpenAI
# import os

# Puedes usar la misma instancia que en open_ai.py o crear una nueva
# Si deseas la misma instancia:
# from open_ai import client as openai_client

# En caso de que quieras instanciar un nuevo cliente:
client = OpenAI()

def hr_analysis(candidate_text: str) -> str:
    """
    Analiza el texto de un candidato desde la perspectiva de RRHH,
    generando conclusiones de soft skills, cultura organizacional, 
    actitudes, etc.

    Retorna un nuevo bloque de texto que complementa la información del candidato.
    """
    # Prompt de ejemplo con 'system' orientado a RRHH
    system_prompt = (
        "Eres un asesor especializado en recursos humanos, con amplia experiencia "
        "en reclutamiento y selección de personal. Tu objetivo es analizar las "
        "soft skills y la compatibilidad cultural de un candidato con la empresa."
        "Se te proporcionará un texto que describe el perfil de la persona "
        "(extraído de su CV o de un análisis previo). Tu respuesta debe:"
        "1. Incluir conclusiones de RR.HH. en un lenguaje claro y empático."
        "2. Resaltar habilidades blandas, actitudes y valores que faciliten "
        "   la adaptación al entorno de la empresa."
        "3. Indicar la compatibilidad cultural y social con la organización."
        "Habla en primera persona plural, como el equipo de RR.HH., "
        "enfatizando la relevancia de la personalidad y la actitud profesional "
        "en el éxito a largo plazo del candidato."
    )

    # Construimos el mensaje
    user_prompt = f"Analiza al candidato de forma resumida enfocada en aspectos de RR.HH.\n\n{candidate_text}"

    try:
        completion = client.chat.completions.create(
            # model="gpt-4o",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        response_text = completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"❌ Error en hr_analysis: {e}")
        return "Error al generar análisis de RR.HH."
