# open_ai.py

from openai import OpenAI

client = OpenAI()

def ai_consult(data):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": data
                }
            ]
        )

        haiku = completion.choices[0].message.content
        return haiku
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
