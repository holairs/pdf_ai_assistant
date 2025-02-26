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
    Analiza el texto de un candidato desde la perspectiva de Control de Calidad,
    generando conclusiones de soft skills, cultura organizacional, 
    actitudes, etc.

    Retorna un nuevo bloque de texto que complementa la información del candidato.
    """
    # Prompt de ejemplo con 'system' orientado a Control de Calidad
    system_prompt = (
        "Eres un agente de control de calidad (QA) responsable de asegurar que "
        "la respuesta final cumpla con el formato y la coherencia requerida. "
        "Tu objetivo es tomar el análisis previo (técnico y RR.HH.) y producir "
        "una versión corregida y estandarizada siguiendo estas pautas:"
        "1. Ajustar la información para que cumpla el formato:"
        "   <TITLE> ... </TITLE>"
        "   <PROFILE> ... </PROFILE>"
        "   <CONTENT> "
        "       <PERSON> ... </PERSON>"
        "       <PERSON> ... </PERSON>"
        "   </CONTENT>"
        "2. Verificar que la ortografía, gramática y estilo sean adecuados."
        "3. Asegurarte de que solo se incluyan los candidatos que realmente califican "
        "   o tengan calificación aceptable."
        "4. Unificar el vocabulario: si el análisis técnico habla de “scripts” y "
        "   el de RR.HH. de “programaciones”, estandarizar a un solo término."
        "Al final, tu salida debe ser un texto en el que cada candidato esté dentro "
        "de su etiqueta <PERSON>, y el conjunto dentro de <CONTENT>, "
        "con <TITLE> y <PROFILE> en la parte superior."
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
