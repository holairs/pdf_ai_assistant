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
                        "   - La calificacion debe de ser en base a que tan adecuado es el candidato para la posición solicitada. "
                        "   - Usa listas, negritas y encabezados cuando sea necesario para mejorar la legibilidad. "
                        
                        "   - Ejemplo: "
                        "     <CONTENT> "
                        "     <PERSON> "
                        "     **Nombre:** Juan Pérez  "
                        "     **Puesto:** Desarrollador Backend con Rust  "
                        "     **Correo:** juan.perez@url_que_indique_su_perfil.com  "
                        "     **Calificación:** 7.0/10  "
                        "     **Experiencia Relevante:**  "
                        "     * Más de 5 años en desarrollo backend con Rust.  "
                        "     * Experiencia en optimización de memoria y concurrencia segura.  "
                        "     * Implementación de APIs robustas y escalables.  "
                        "     **Conclusión:**  "
                        "     Juan Pérez es un candidato altamente calificado para esta posición.  "
                        "     </PERSON> "
                        "     </CONTENT> "
                        
                        " **Requisitos adicionales:** "
                        "- Mantén la respuesta concisa y enfocada solo en la información relevante para la posición solicitada. "
                        "- No incluyas explicaciones innecesarias o candidatos que no cumplen con los requisitos. "
                        "- Si un candidato tiene calificacion baja pero no hay muchos candidatos, incluirlo en la respuesta. "
                        "- Asegura que cada perfil esté **bien redactado y parezca un CV generado profesionalmente**. "
                        "- Se lo mas extenso posible en la información de cada candidato, siempre resaltando el enfoque de la solicitud de la consulta. "
                        "- Si tiene certificaciones acorde al puesto, incluirlo en la información del candidato. "
                        "- **El formato de salida debe ser consistente** para permitir su almacenamiento en una base de datos y su posterior conversión a PDF."
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
