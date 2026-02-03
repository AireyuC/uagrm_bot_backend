import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_openai_response(user_text, context_text=""):
    """
    Envía el mensaje a OpenAI con un contexto académico inyectado.
    """
    system_prompt = "Eres un asistente útil de la UAGRM. Responde basándote estrictamente en el contexto proporcionado. Ordena la información de manera clara y concisa."
    
    # Construimos el mensaje completo con el contexto
    messages = [
        {"role": "system", "content": f"{system_prompt}\n\nCONTEXTO:\n{context_text}"},
        {"role": "user", "content": user_text}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # O "gpt-3.5-turbo" si prefieres
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        bot_reply = response.choices[0].message.content.strip()
        tokens = response.usage.total_tokens if response.usage else 0
        
        return bot_reply, tokens

    except Exception as e:
        print(f"Error OpenAI: {e}")
        return "Lo siento, hubo un error al conectar con la IA.", 0
