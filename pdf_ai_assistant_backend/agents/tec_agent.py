# project/agents/hr_agent.py

from openai import OpenAI
# import os

# Puedes usar la misma instancia que en open_ai.py o crear una nueva
# Si deseas la misma instancia:
# from open_ai import client as openai_client

# En caso de que quieras instanciar un nuevo cliente:
client = OpenAI()

def tec_analysis(candidate_text: str) -> str:
    """
    Analiza el texto de un candidato desde la perspectiva de RRHH,
    generando conclusiones de soft skills, cultura organizacional, 
    actitudes, etc.

    Retorna un nuevo bloque de texto que complementa la información del candidato.
    """
    # Prompt de ejemplo con 'system' orientado a perfil Técnico
    system_prompt = (
        "Eres un asesor técnico especializado en el área de desarrollo de software. "
        "Te enfocas en evaluar la competencia profesional del candidato con respecto "
        "a lenguajes de programación, frameworks, proyectos relevantes, arquitecturas "
        "de software y cualquier habilidad técnica específica."
        "Tu respuesta debe:"
        "1. Analizar la experiencia técnica del candidato en base al CV o "
        "   texto proporcionado, enfatizando lenguajes y frameworks clave."
        "2. Describir el nivel estimado de dominio en esas tecnologías."
        "3. Identificar posibles gaps técnicos y certificaciones o logros "
        "   sobresalientes en el área."
        "4. Ser concisa pero detallada, utilizando un lenguaje formal y orientado "
        "   a los responsables de proyecto o arquitectos de software."
        "Evita evaluar soft skills; tu objetivo es únicamente la parte técnica. "
        "Utiliza un tono directo y profesional."
    )

    # Construimos el mensaje
    user_prompt = f"Analiza al candidato de forma resumida enfocada en aspectos técnicos.\n\n{candidate_text}"

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
