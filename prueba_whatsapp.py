import requests
import json

# CONFIGURACIÓN
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = "/api/chat/post/"

# TU NÚMERO REGISTRADO (Tal cual lo pusiste en el Admin)
# Si en el admin pusiste "59177777777", aquí pon lo mismo.
MI_CELULAR = "59164601410" 

def simular_n8n():
    print(f"--- 📱 SIMULANDO MENSAJE DESDE WHATSAPP/N8N ---")
    print(f"Enviando desde: {MI_CELULAR}")
    
    # 1. Prueba de consulta personal (Debería dar notas)
    mensaje_1 = "¿Cómo voy en mis materias?"
    payload = {
        "message": mensaje_1,
        "phone": MI_CELULAR
        # NOTA: No estamos enviando Token ni Header de Authorization
    }
    
    print(f"\n1️ Enviando: '{mensaje_1}'...")
    try:
        response = requests.post(f"{BASE_URL}{ENDPOINT}", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("RESPUESTA DEL BOT:\n")
            print(data.get('response', data))
        else:
            print(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Error de conexión: {e}")

    # 2. Prueba de número desconocido (Para verificar seguridad)
    print("\n------------------------------------------------")
    print("2 Probando con un número falso (Invitado)...")
    payload_fake = {
        "message": "¿Cómo voy en mis materias?",
        "phone": "00000000" 
    }
    
    response = requests.post(f"{BASE_URL}{ENDPOINT}", json=payload_fake)
    print("RESPUESTA DEL BOT (Debería ser genérica/rechazo):\n")
    print(response.json().get('response', response))

if __name__ == "__main__":
    simular_n8n()