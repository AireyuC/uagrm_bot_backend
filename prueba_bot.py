import requests
import sys

# CONFIGURACIÓN
BASE_URL = "http://127.0.0.1:8000"
USERNAME = "Carlos"     # <--- Pon aquí el usuario que creaste en Admin
PASSWORD = "aireyu123"    # <--- Pon aquí la contraseña

def probar_chatbot():
    print(f"--- 1. INTENTANDO LOGIN CON {USERNAME} ---")
    
    url_login = f"{BASE_URL}/api/auth/login/" 
    
    try:
        response = requests.post(url_login, json={
            "username": USERNAME, 
            "password": PASSWORD
        })
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token') or data.get('access') or data.get('key')
            print("✅ Login Exitoso. Iniciando chat...")
        else:
            print(f"❌ Error en Login: {response.text}")
            return

    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        return

    # ---------------------------------------------------------
    url_chat = f"{BASE_URL}/api/chat/post/"
    headers = {
        "Authorization": f"Token {token}"
    }

    print("\n💬 CHAT INICIADO (Escribe 'salir' para terminar)")
    print("-------------------------------------------------")

    while True:
        try:
            pregunta = input("\n👤 Tú: ")
        except UnicodeDecodeError:
            # Fallback para errores de encoding en consola Windows a veces
            pregunta = input("\n👤 Tú: ")

        if pregunta.lower() in ["salir", "exit"]:
            print("¡Hasta luego! 👋")
            break
        
        if not pregunta.strip():
            continue

        try:
            chat_response = requests.post(url_chat, json={"message": pregunta}, headers=headers)
            
            if chat_response.status_code == 200:
                respuesta = chat_response.json()
                bot_msg = respuesta.get('response', respuesta)
                print(f"🤖 Bot: {bot_msg}")
            else:
                print(f"❌ Error del Bot: {chat_response.text}")
        except Exception as e:
             print(f"❌ Error en la petición: {e}")

if __name__ == "__main__":
    # Forzar encoding utf-8 en consola Windows por si acaso
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    probar_chatbot()