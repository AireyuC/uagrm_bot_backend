# 📘 Guía Técnica: Configuración de n8n y WhatsApp API (v3.0)

**Proyecto:** Chatbot Institucional UAGRM  
**Versión de API Meta:** v24.0  
**Herramienta de Orquestación:** n8n (Docker)

Esta guía detalla paso a paso cómo configurar la integración entre WhatsApp (Meta), n8n y el Backend Django. Sigue este orden estrictamente para evitar errores de conexión.

---

## 🏗️ Parte 1: Configuración en Meta (Facebook Developers)
Antes de tocar n8n, necesitamos preparar el entorno en Meta.

### 1. Requisitos Previos (Portafolio Comercial)
Meta exige una estructura burocrática. Necesitas una **Cuenta de Desarrollador** y un **Portafolio Comercial** (Business Portfolio).

> **Nota Importante:** Utiliza una cuenta limpia o existente, pero verifica que tengas menos de 4 portafolios creados. Meta tiene un límite estricto y si llegas al límite, no te dejará crear la App.

### 2. Creación de la App
1. Ve a [developers.facebook.com](https://developers.facebook.com).
2. Crea una **nueva App**.
3. **Tipo de App:** Selecciona **Empresa** (Business).
4. Asocia la App al Portafolio Comercial que elegiste.
5. Una vez creada, busca el producto **WhatsApp** y dale a "Configurar" (Set up).

### 3. Panel de Configuración API (API Setup)
En el menú lateral: **WhatsApp > API Setup**. Aquí encontrarás 3 datos vitales:

- **Token de Acceso Temporal:** Caduca cada 24 horas. (Para producción se necesitará un token permanente de sistema).
- **Identificador de Número de Teléfono (Phone Number ID):** Es el ID del número que enviará los mensajes (el bot). **Cópialo.**
- **Número de Prueba:** El número desde el cual puedes enviar mensajes sin pagar (sandbox).

---

## 🤝 Parte 2: El "Handshake" (Verificación del Webhook)
Este es el paso crítico donde Meta y n8n se conectan por primera vez.

### Paso A: Preparar n8n en Modo "Escucha" (GET)
Para que Meta verifique tu servidor, n8n debe responder un código secreto (Challenge).

1. Abre el nodo **Webhook** en n8n.
2. Configura **HTTP Method:** `GET`.
3. Abre el nodo **Respond to Webhook**.
4. En **Response Body**, coloca esta expresión: 
   ```javascript
   {{ $json.query['hub.challenge'] }}
   ```
5. **ACTIVA EL FLUJO** (Switch verde arriba a la derecha).

### Paso B: Configurar en Meta
1. En el panel de Meta, ve a **WhatsApp > Configuration**.
2. Busca la sección **Webhook** y dale a **Edit**.
3. **Callback URL:** Pega tu dirección de Ngrok pública + el path configurado en n8n.  
   *Ejemplo:* `https://tu-ngrok.ngrok-free.app/webhook/whatsapp`
4. **Verify Token:** Inventa una contraseña propia (Ej: `uagrm_secret_123`).
   > *Nota: Esta contraseña es para que tú verifiques que la solicitud viene de Meta. Puedes poner cualquiera ahora.*
5. **¡Verificar y Guardar!**
   - Dale clic al botón. Si n8n está activo y en modo GET, Meta mostrará un check verde ✅.
   - **Verificación:** Ve a la pestaña "Executions" en n8n; deberías ver una ejecución exitosa.

### Paso C: Suscripción a Eventos (Webhook Fields)
Una vez verificado:
1. En la misma sección de configuración de Meta, busca **Webhook Fields**.
2. Dale a **Manage**.
3. Busca y suscríbete (**Subscribe**) a: `messages`.
   > *Si no haces esto, Meta no enviará nada cuando un usuario escriba.*

### Paso D: Volver n8n a Modo Producción (POST)
Una vez hecho el handshake, n8n debe dejar de saludar y empezar a trabajar.

1. **Apaga** el flujo n8n.
2. Cambia el Webhook a `POST`.
3. Cambia el Respond to Webhook a responder simplemente `OK`.
4. Vuelve a **ACTIVAR** el flujo.

---

## ⚙️ Parte 3: Configuración de Nodos en n8n (Paso a Paso)
Configuración detallada para la versión actual del flujo.

### 🟢 Nodo 1: Webhook (Entrada)
- **Authentication:** None
- **HTTP Method:** `POST` (Obligatorio para recibir mensajes).
- **Path:** `whatsapp` (O el nombre que prefieras, pero debe coincidir con la URL en Meta).
- **Respond:** Using 'Respond to Webhook' Node.

### 🟢 Nodo 2: Respond to Webhook (Anti-Bloqueo)
Responde inmediatamente a Meta para evitar timeouts.
- **Respond With:** Text.
- **Response Body:** `OK`.
- **Options:** Agregar **Response Code** y poner `200`.

### 🟢 Nodo 3: If (Filtro de Mensajes)
Solo deja pasar mensajes nuevos, ignora estados de lectura.
- **Condition:** Array (Importante: No usar String).
- **Value 1:** 
  ```javascript
  {{ $json.body.entry[0].changes[0].value.messages }}
  ```
- **Operation:** Is Not Empty.

### 🟢 Nodo 4: HTTP Request (Hacia Django)
Envía los datos al Backend Dockerizado.
- **Method:** `POST`.
- **URL:** `http://web:8000/api/chat/post/`  
  *(Nota: `web` es el nombre del servicio en Docker. Agregar `/post/` al final).*
- **Authentication:** None.
- **Send Body:** Activado.
- **Content Type:** JSON.
- **Specify Body:** Using Fields Below.
  - **Field 1:** Name `message` | Value `{{ $json.body.entry[0].changes[0].value.messages[0].text.body }}`
  - **Field 2:** Name `phone` | Value `{{ $json.body.entry[0].changes[0].value.messages[0].from }}`

### 🟢 Nodo 5: HTTP Request (Hacia WhatsApp API v24.0)
Envía la respuesta final al usuario.
- **Method:** `POST`.
- **URL:** `https://graph.facebook.com/v24.0/TU_IDENTIFICADOR_DE_TELEFONO/messages`
  *(Reemplaza `TU_IDENTIFICADOR...` con el ID numérico de tu panel Meta).*
- **Authentication:** None (Lo haremos manual en Headers).
- **Send Query Parameters:** Activado.
- **Specify Headers:** Using Fields Below.
  - **Name:** `Authorization`
  - **Value:** `Bearer TU_TOKEN_DE_META`  
  *(Recuerda: Si el token caduca, debes generarlo de nuevo en Meta y actualizarlo aquí).*
- **Send Body:** Activado.
- **Body Content Type:** JSON.
- **Specify Body:** Using JSON.
- **JSON Code:**
  ```json
  {
    "messaging_product": "whatsapp",
    "to": "{{ $node['Webhook'].json.body.entry[0].changes[0].value.messages[0].from }}",
    "text": {
      "body": "{{ $json.response }}"
    }
  }
  ```

---

## 💾 Respaldo y Restauración (Importante)
No confíes en la memoria del contenedor. Guarda tu trabajo frecuentemente.

**Cómo descargar el flujo:**
1. En el editor de n8n, mira a la esquina superior derecha (lado izquierdo del logo de GitHub/Usuario).
2. Haz clic en los 3 puntos (...).
3. Selecciona **Download** (o Export Workflow).
4. Guarda el archivo `.json` en una carpeta segura fuera de Docker.

**Cómo restaurar:**
1. En el mismo menú de los 3 puntos.
2. Selecciona **Import from File**.
3. Carga tu `.json` y el flujo aparecerá tal cual lo dejaste.

---

## ⚠️ Solución de Problemas Comunes
- **Error 404 en Django:** Verifica que la URL en el Nodo 4 termine en `/post/`.
- **Meta no envía mensajes:** Verifica que te suscribiste al evento `messages` en la configuración del Webhook en Meta.
- **Error de Token (401 Unauthorized):** El token temporal de 24h caducó. Ve al panel de Meta, genera uno nuevo y pégalo en el Nodo 5 (Header Authorization).