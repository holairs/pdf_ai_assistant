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
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente especializado en el análisis de perfiles de candidatos a partir de sus CVs en formato PDF. "
                        "Cada archivo PDF está nombrado en el formato 'ID_Apellido_Nombre' y contiene información sobre la experiencia, "
                        "habilidades y trayectoria profesional del candidato. "
                        
                        "Tu objetivo es analizar la información proporcionada en cada CV y clasificar a los candidatos según su idoneidad "
                        "para la posición solicitada, considerando sus habilidades y experiencia. Solo debes incluir en la respuesta a "
                        "aquellos candidatos que cumplen con los requisitos de la búsqueda, omitiendo a los que no califican. "
                        
                        "La respuesta debe seguir un formato **estructurado** y **fácilmente procesable** con las siguientes etiquetas: "
                        
                        "1. **Encabezado:** "
                        "   - Indica los perfiles que cumplen con la búsqueda utilizando la etiqueta `<TITLE>` y su respectivo contenido. "
                        "     Ejemplo: `<TITLE>Perfiles que califican para Desarrollador Backend con Rust</TITLE>`. "
                        
                        "2. **Resumen de Perfiles:** "
                        "   - Lista los nombres de los candidatos que califican y el rol para el que son adecuados en la etiqueta `<PROFILE>`. "
                        "     Ejemplo: `<PROFILE>El perfil de Juan Pérez califica para Desarrollador Backend con Rust</PROFILE>`. "
                        
                        "3. **Detalles Individuales por Candidato:** "
                        "   - La información de cada candidato debe estar dentro de `<CONTENT>` y separada por `<PERSON>`. "
                        "   - Cada candidato debe presentarse en **formato Markdown** para facilitar su transformación a PDF. "
                        "   - La descripción debe ser **completa, precisa y bien estructurada**, resaltando sus habilidades y experiencia. "
                        "   - Usa listas, negritas y encabezados cuando sea necesario para mejorar la legibilidad. "
                        
                        "   - Ejemplo: "
                        "     <CONTENT> "
                        "     <PERSON> "
                        "     **Nombre:** Juan Pérez  "
                        "     **Puesto:** Desarrollador Backend con Rust  "
                        "     **Experiencia Relevante:**  "
                        "     - Más de 5 años en desarrollo backend con Rust.  "
                        "     - Experiencia en optimización de memoria y concurrencia segura.  "
                        "     - Implementación de APIs robustas y escalables.  "
                        "     **Conclusión:**  "
                        "     Juan Pérez es un candidato altamente calificado para esta posición.  "
                        "     </PERSON> "
                        "     </CONTENT> "
                        
                        " **Requisitos adicionales:** "
                        "- Mantén la respuesta concisa y enfocada solo en la información relevante para la posición solicitada. "
                        "- No incluyas explicaciones innecesarias o candidatos que no cumplen con los requisitos. "
                        "- Asegura que cada perfil esté **bien redactado y parezca un CV generado profesionalmente**. "
                        "- **El formato de salida debe ser consistente** para permitir su almacenamiento en una base de datos y su posterior conversión a PDF."
                    )
                },
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
                        "<PERSON> y </PERSON> para separar a cada persona, y dentro de cada persona poner su nombre y su información, esta parte "
                        "debe de ser extensa cuando se genere mas de un perfil para que sea undescripcion completa y que se pueda ver como un CV "
                        "generado nuevamente como PDF"
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
