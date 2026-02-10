# Estructura del Proyecto UAGRM Bot

Este documento describe la organización de carpetas y archivos del repositorio para facilitar la navegación a nuevos desarrolladores.

## 📂 Árbol de Directorios

```text
uagrm_bot_backend/
├── 📂 apps/                  # Módulos de la aplicación (Domain Driven Design ligero)
│   ├── 📂 authentication/    # [Legacy v2.0] Gestión de usuarios y tokens
│   ├── 📂 chatbot/           # [Core] Lógica del asistente, RAG y Webhooks
│   ├── 📂 institutional/     # [Core] Gestión de documentos, LlamaParse y Vectores
│   └── 📂 simulation/        # [Legacy v2.0] Mock API del sistema académico
│
├── 📂 config/                # Configuración global del proyecto Django
│   ├── 📂 settings/          # Configuraciones divididas (base, local, prod)
│   ├── asgi.py               # Entrada para servidor asíncrono (Prod)
│   ├── urls.py               # Enrutador principal (Main Router)
│   └── wsgi.py               # Entrada para servidor WSGI estándar
│
├── 📂 core/                  # Utilidades transversales y vistas base
├── 📂 documentos/            # [Ignorado] Carpeta temporal para procesamiento de docs
├── 📂 pdfs/                  # [Ignorado] Almacenamiento local de PDFs de prueba/ingesta
├── 📂 templates/             # Plantillas HTML (Django Templates)
├── 📂 utils/                 # Funciones auxiliares y excepciones custom
│
├── .env                      # Variables de entorno (NO subir al repo)
├── .gitignore                # Archivos ignorados por Git
├── debug_kb.py               # Script de utilidad para probar la base de conocimientos
├── docker-compose.yml        # Orquestación de contenedores (App + DB)
├── Dockerfile                # Definición de la imagen de la App
├── manage.py                 # CLI principal de Django
├── README.md                 # Documentación técnica general
└── requirements.txt          # Dependencias de Python


[Ignorado = carpetas locales para procesamiento de documentos]

```

---

## 📘 Descripción Detallada

### 1. Raíz (`/`)
Contiene los archivos de configuración de infraestructura y orquestación.
*   **`docker-compose.yml`**: Define los servicios necesarios (Web App, PostgreSQL con pgvector).
*   **`manage.py`**: Script de entrada para ejecutar comandos de Django (`runserver`, `migrate`, `createsuperuser`).

### 2. Configuración (`config/`)
El corazón de la configuración del framework.
*   **`settings/`**:
    *   `base.py`: Configuraciones comunes (Apps instaladas, Middleware, Constantes).
    *   `local.py` / `production.py`: Sobreecrituras específicas por entorno (Debug, BD).
*   **`urls.py`**: Define las rutas principales y mapea las URLs a las diferentes apps (`/api/chat/`, `/api/auth/`).

### 3. Aplicaciones (`apps/`)
Arquitectura modular donde cada carpeta encapsula una funcionalidad específica.

#### 🔐 `apps/authentication/` (Legacy)
Maneja la lógica de usuarios, registro y autenticación vía Tokens.
*   *Nota*: Aunque el sistema opera en "Modo Público", este módulo contiene la estructura de usuarios (CustomUser) necesaria para el admin de Django.

#### 🤖 `apps/chatbot/` (Core System)
El cerebro del bot.
*   **`services/`**:
    *   `ai_handler.py`: Lógica de orquestación (User input -> RAG -> LLM -> Output).
    *   `knowledge_retriever.py`: Lógica de búsqueda vectorial.
*   **`api/`**: Endpoints para recibir mensajes de WhatsApp (Webhooks).
*   **`models/`**: `ChatHistory` (historial de conversaciones).

#### 🏛️ `apps/institutional/` (Core System)
Gestión del conocimiento institucional y documentos.
*   **`services/ingestion.py`**: Pipeline de ingesta (PDF -> LlamaParse -> Chunks -> Embeddings -> PGVector).
*   **`models/`**: `UploadedDocument` (PDF original) y `DocumentChunk` (fragmentos vectorizados).

#### 🎓 `apps/simulation/` (Legacy)
 API simulada para datos académicos.
*   *Estado*: Actualmente inactiva en producción pública, pero útil para desarrollo y pruebas de integración futura con sistemas ERP reales.

### 4. Utilidades y Scripts (`utils/` + Scripts Raíz)
*   **`utils/exceptions.py`**: Manejador global de errores para estandarizar las respuestas JSON de la API.
*   **`debug_kb.py`**: Script independiente para realizar consultas de prueba directa a la Base de Conocimiento (RAG) sin levantar todo el servidor. Útil para diagnósticos rápidos.

### 5. Archivos Estáticos y Plantillas
*   **`templates/`**: Contiene los archivos HTML para las vistas renderizadas por Django (ej. páginas de error, landing pages simples).
*   **`pdfs/`** y **`documentos/`**: Directorios auxiliares utilizados durante el desarrollo para almacenar PDFs de prueba o realizar cargas masivas manuales. *Suelen estar ignorados en git*.
*   *Nota*: Las carpetas `static/` y `media/` no están presentes en el repositorio base; se generan automáticamente al ejecutar `collectstatic` o subir archivos respectivamente.
