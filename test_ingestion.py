import requests
import os

# CONFIGURACIÓN
URL = "http://localhost:8000/api/chat/upload/"
FILE_PATH = "documento_secreto.txt"
# Cambia esto por la API Key que generaste en el Admin de Django
API_KEY = "PON_TU_API_KEY_AQUI" 
CUSTOM_HEADER = "X-Api-Key-Custom" # El nombre que definimos en settings (sin HTTP_)

def crear_archivo_prueba():
    """Crea un archivo de texto dummy para probar."""
    contenido = """
    CONFIDENCIAL: PROYECTO SECRETOS DE LA UAGRM
    
    Este es un documento confidencial sobre el nuevo campus en Marte.
    Si el bot responde sobre esto antes de ser aprobado, el filtro ha fallado.
    
    Contacto de emergencia: admin@uagrm.edu.bo
    Teléfono: 70012345
    """
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"✅ Archivo de prueba creado: {FILE_PATH}")

def subir_archivo():
    if not os.path.exists(FILE_PATH):
        crear_archivo_prueba()

    print(f"📡 Enviando archivo a {URL}...")
    
    try:
        # Abrimos el archivo en modo binario
        with open(FILE_PATH, 'rb') as f:
            files = {'file': f}
            # Headers con la API Key
            headers = {CUSTOM_HEADER: API_KEY}
            
            response = requests.post(URL, headers=headers, files=files)
        
        print(f"\nStatus Code: {response.status_code}")
        try:
            print("Respuesta del Servidor:")
            print(response.json())
        except:
            print(response.text)
            
        if response.status_code == 201:
            print("\n✅ ¡ÉXITO! El documento se subió correctamente.")
            print("👉 Ahora ve al Admin de Django y verifica que esté en estado 'PENDING'.")
        elif response.status_code == 403:
            print("\n⛔ ERROR 403: Permiso denegado.")
            print("Verifica que tu API KEY sea correcta y que la hayas puesto en la variable API_KEY del script.")
        else:
            print("\n❌ Algo salió mal.")

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        print("Asegúrate de que el servidor esté corriendo (python manage.py runserver)")

if __name__ == "__main__":
    # Verificación simple de requests
    try:
        import requests
    except ImportError:
        print("Falta la librería 'requests'. Instálala con: pip install requests")
        exit(1)

    auth_input = input(f"Ingresa tu API Key (Enter para usar '{API_KEY}'): ").strip()
    if auth_input:
        API_KEY = auth_input

    subir_archivo()
