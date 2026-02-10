# Documentación Técnica del Sistema UAGRM Bot (Modo Público)

## 1. Visión General

El **UAGRM Bot** es un sistema de consultas automatizadas basado en **RAG (Retrieval-Augmented Generation)**. Su objetivo principal es responder preguntas institucionales, académicas y administrativas a través de WhatsApp, utilizando información oficial extraída de documentos PDF subidos por la universidad.

> [!NOTE]
> **Modo Actual**: El sistema opera en **Modo Público Estricto**. No requiere inicio de sesión y responde a cualquier usuario con información de acceso público.

---

## 2. Arquitectura de Ingesta y Conocimiento

El núcleo del conocimiento del bot proviene de documentos PDF procesados y vectorizados.

### Proceso de Ingesta (ETL)
1. **Extracción (LlamaParse)**: Los documentos PDF subidos al panel administrativo son procesados por `LlamaParse`. Esta herramienta convierte el contenido visual (texto, tablas, encabezados) en formato Markdown estructurado, preservando la jerarquía de la información.
2. **Fragmentación (Chunking)**: El texto Markdown se divide en fragmentos lógicos (chunks) para optimizar la búsqueda semántica.
3. **Indexado Vectorial (PGVector)**: Cada chunk se convierte en un vector numérico (embedding) utilizando modelos de OpenAI (`text-embedding-3-small`) y se almacena en una base de datos PostgreSQL con la extensión `pgvector`.

---

## 3. Módulo de Chatbot (Core)

El flujo de interacción es el siguiente:

1. **Recepción del Mensaje**: El usuario envía una consulta vía WhatsApp (o API directa).
2. **RAG Retrieval (Búsqueda)**:
    - El sistema convierte la pregunta del usuario en un vector.
    - Busca en `PGVector` los fragmentos de conocimiento más similares semánticamente.
    - Se filtran los resultados para asegurar que solo se use información con `access_level='public'`.
3. **Síntesis (LLM)**:
    - Se construye un prompt que incluye: Instrucciones del sistema + Contexto recuperado (fragmentos) + Pregunta del usuario.
    - Se envía a **OpenAI (GPT-4o-mini)** para generar una respuesta natural y precisa.
4. **Respuesta**: El bot envía la respuesta generada al usuario.

### Autenticación y Roles (Legacy / Deprecated)
> [!WARNING]
> Existe código en el sistema (`StudentConnection`, `MockStudent`) diseñado para autenticación de estudiantes y consultas de datos privados (notas, deudas). **Esta lógica está actualmente DESACTIVADA y COMENTADA** en el código fuente para garantizar el funcionamiento 100% público. Si se descomenta, el sistema tiene la capacidad de manejar roles (`student`, `teacher`) y restringir el acceso a cierta información.

---

## 4. Módulo de Simulación (Mock API)

El proyecto incluye aplicaciones (`apps.simulation`) con modelos como `MockStudent`, `MockAcademicRecord` y `MockFinancialStatus`.
*   **Estado Actual**: **Inactivo**.
*   **Propósito Original**: Simular una base de datos universitaria externa (ERP) para pruebas de desarrollo sin conectar a sistemas reales.

---

## 5. Guía de Despliegue Rápido

Para levantar el sistema en un entorno nuevo:

1. **Requisitos**: Docker y Docker Compose instalados.
2. **Configuración**:
    - Crear un archivo `.env` basado en `.env.example`.
    - Definir `OPENAI_API_KEY` y credenciales de base de datos.
3. **Ejecución**:
    ```bash
    docker-compose up -d --build
    ```
4. **Migraciones**:
    ```bash
    docker-compose exec web python manage.py migrate
    ```
5. **Carga de Datos (Opcional)**:
    Ingresar al admin panel (`/admin/`) para subir documentos PDF y alimentar la base de conocimiento.
