# UAGRM Bot Backend

Backend oficial para el Chatbot Universitario de la UAGRM. Desarrollado con Django Rest Framework e Inteligencia Artificial (OpenAI).

## 🚀 Características

*   **Autenticación**: Sistema de Login con Roles (Estudiante/Docente) y Tokens.
*   **Chatbot RAG**:
    *   **Contexto Académico**: Notas y perfil del estudiante (simulado).
    *   **Contexto Institucional**: Búsqueda en base de conocimientos (Reglamentos, Fechas).
*   **Documentación API**: Swagger/OpenAPI integrado.
*   **Demo Web**: Interfaz de chat lista para probar.

## 🛠️ Tecnologías

*   Python 3.x
*   Django 5.0 + DRF
*   PostgreSQL
*   OpenAI API (GPT-4o / GPT-4o-mini)
*   Docker (Opcional)

## ⚙️ Instalación y Configuración

1.  **Clonar el repositorio**
    ```bash
    git clone https://github.com/TU_USUARIO/uagrm_bot_backend.git
    cd uagrm_bot_backend
    ```

2.  **Crear entorno virtual**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno (.env)**
    Crea un archivo `.env` en la raíz (basado en el ejemplo):
    ```ini
    DEBUG=True
    SECRET_KEY=tu_clave_secreta_segura
    OPENAI_API_KEY=sk-proj-... (Tu Key de OpenAI)
    
    # Base de Datos
    DB_NAME=uagrm_bot_db
    DB_USER=postgres
    DB_PASSWORD=tu_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

5.  **Base de Datos**
    Asegúrate de tener PostgreSQL corriendo y la base de datos creada.
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

## ▶️ Ejecución

Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

## 🔗 Enlaces de Interés

*   **Demo Chat**: [http://127.0.0.1:8000/demo/](http://127.0.0.1:8000/demo/)
    *   Prueba el flujo completo de Login + Chat.
*   **Documentación API (Swagger)**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
    *   Explora todos los endpoints disponibles.
*   **Panel Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    *   Gestiona usuarios, notas simuladas y base de conocimiento.

## 🧪 Testing

Puedes usar el script interactivo incluido para probar desde la terminal:
```bash
python prueba_bot.py
```
