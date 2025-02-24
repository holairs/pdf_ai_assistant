# open_ai.py

from openai import OpenAI

client = OpenAI()

def ai_consult(data: dict):
    try:
        # Asegurar que las claves existen en el diccionario
        prompt = data.get("prompt", "No prompt provided.")
        pdfs_content = "\n\n".join([f"{name}:\n{text}" for name, text in data.get("pdfs", {}).items()])

        # Construir el mensaje que se enviará a OpenAI
        message_content = f"{prompt}\n\nDocumentos analizados:\n{pdfs_content}"

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                # {
                #     "role": "system",
                #     "content": (
                #         "Eres una IA especializada en analizar perfiles de candidatos "
                #         "a partir de sus CVs en formato PDF. Cada PDF se nombra con el "
                #         "formato 'ID_Apellido_Nombre' y contiene la información sobre "
                #         "su experiencia, habilidades y trayectoria. Tu objetivo es, con "
                #         "con base en las instrucciones que recibas, revisar la información "
                #         "de cada uno y clasificar a los candidatos "
                #         "según su idoneidad, habilidades y/o experiencia. Al final, "
                #         "debes devolver la clasificación como una lista donde indiques, "
                #         "para cada archivo, el ID y el nombre del candidato, así como "
                #         "el resultado de tu análisis,seras breve con cada respuesta,"
                #         "no indagues en tanta explicacion sin tanto enrollo, "
                #         "y no menciónes a los que no califican para la petición"
                #         "cuando te pida varias personas otorgalas, cuando te pida"
                #         "solo una persona, solo da la inforamcion de una persona"
                #         "todo en español y en formato markdown sin poner "
                #         "la triple comilla que indica que es markdown al inicio  y a al final, y que lo des como un listado"
                #         "cada persona con su titulo y analisis, pero no mezcles a las personas"
                #         "pon a cada persona en su propio espacio"
                #     )
                # },
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente especialiazado en analizar perfiles de candidatos"
                        "a partir de sus CVs en formato PDF. Cada PDF se nombra con el "
                        "formato 'ID_Apellido_Nombre' y contiene la información sobre "
                        "su experiencia, habilidades y trayectoria. Tu objetivo es, con "
                        "con base en las instrucciones que recibas, revisar la información "
                        "de cada uno y clasificar a los candidatos "
                        "según su idoneidad, habilidades y/o experiencia. Al final, "
                        "debes devolver la clasificación como un un pdf nuevo cada candidato, "
                        "basado en lo que el candidato ya tiene en su CV, es decir, regresaras un pdf "
                        "pero regresarás la información para poder separarla por un pdf por candidato "
                        "en formato markdown para luego poder transformarla manualmente a pdf "
                        "pero resaltarás las partes en las que el candidato muestra las habilidades "
                        "que se han solicitado en la busqueda de perfil, puedes ser exteneso con esa descripcion "
                        "pero no te vayas por las ramas, solo lo que se solicita, y no menciones a los que no califican "
                        "para la petición, solo a los que si califican, en la response pondrás un separador de respuesta "
                        "para poder separarlo mas adelante y guardar la información en una base de datos "
                        "como encabezado dirás este perfil o estos perfiles (dependiendo al caso) clafician para [nombre de la busqueda que quede como un título adecuado no tan largo] "
                        "eso puedes ponerlo como markdown pero dentro de un tag manual como <TITLE> y </TITLE> "
                        "ahora abajo de ello otro separado en otro tag manual como <PROFILE> y </PROFILE>  pondras "
                        "El perfil o perfiles de [nombre de las personas que califican] califican para [nombre de la busqueda que quede como un título adecuado no tan largo] "
                        "ahora separado por un tag manual <CONTENT> y </CONTENT> pondras la información de cada persona que califica "
                        "En formato markdown de manera separada, pero no mezcles a las personas, pon a cada persona en su propio espacio "
                        "para luego transforma esta parte en un pdf individual por cada persona que califica, puedes poner un sub tag manual "
                        "<PERSON> y </PERSON> para separar a cada persona, y dentro de cada persona poner su nombre y su información "
                        )
                },
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        )

        response_text = completion.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"❌ Error en OpenAI API: {e}")
        return {"error": str(e)}
