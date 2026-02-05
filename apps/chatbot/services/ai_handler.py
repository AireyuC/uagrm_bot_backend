import openai
from django.conf import settings
from apps.chatbot.models import StudentConnection
from apps.simulation.models import MockStudent, MockAcademicRecord, MockFinancialStatus
from apps.chatbot.services.knowledge_retriever import search_knowledge_base

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

def procesar_mensaje(telefono, mensaje_usuario):
    """
    Controlador principal del Chatbot.
    """
    # 0. Limpieza y Normalización
    user_msg_lower = mensaje_usuario.strip().lower()
    
    # Debug: Ver qué llega realmente (Míralo en tu terminal)
    print(f"Mensaje recibido: '{user_msg_lower}' de {telefono}")

    # --- COMANDO DE SALIDA (Lógica Mejorada) ---
    # Lista de palabras gatillo
    comandos_salida = ["salir", "cerrar sesion", "cerrar sesión", "desvincular", "logout", "cerrar cuenta"]
    
    # Buscamos si ALGUNA de las palabras clave está en el mensaje
    if any(cmd in user_msg_lower for cmd in comandos_salida):
        print(f"Detectado intento de salida: {telefono}")
        try:
            # Intentamos borrar. Usamos 'filter().delete()' porque si no existe, no da error.
            deleted_count, _ = StudentConnection.objects.filter(phone_number=telefono).delete()
            
            if deleted_count > 0:
                return "✅ **Sesión cerrada correctamente.**\n\nTu cuenta ha sido desvinculada. Para ver tus notas nuevamente, tendrás que iniciar sesión.", 0
            else:
                return "⚠️ No tenías ninguna sesión activa, pero todo está en orden.", 0
                
        except Exception as e:
            print(f"Error logout: {e}")
            return "Hubo un error técnico al intentar cerrar sesión.", 0
    
    # 1. Detectar si es consulta privada
    intenciones_privadas = ["notas", "nota", "promedio", "deuda", "monto", "pagar", "horario", "mis materias", "boleta"]
    es_privado = any(word in user_msg_lower for word in intenciones_privadas)
    
    # 2. Verificar si está autenticado
    usuario_autenticado = False
    registro_estudiante = None
    
    if telefono:
        try:
            # Asegúrate que el telefono coincida exactamente con lo guardado en DB
            # A veces llega con '+' y en la base está sin '+', o viceversa.
            conexion = StudentConnection.objects.get(phone_number=telefono, is_active=True)
            usuario_autenticado = True
            registro_estudiante = conexion.student_id
        except StudentConnection.DoesNotExist:
            usuario_autenticado = False

    # 3. EL MURO DE LOGIN
    if es_privado and not usuario_autenticado:
        # Ajusta esto a tu IP real si lo pruebas desde celular (no localhost)
        base_url = "http://localhost:8000" 
        login_url = f"{base_url}/api/chat/link/?phone={telefono}" # <--- OJO: Ajusté la ruta a la que definimos antes
        
        return f"🔒 **Acceso Restringido**\n\nPara ver esa información personal, necesito verificar tu identidad una única vez.\n\nPor favor, vincula tu cuenta aquí:\n👉 {login_url}", 0

    # 4. SI PASA EL MURO Y ES CONSULTA PRIVADA (Mock API)
    if usuario_autenticado and es_privado:
        try:
            estudiante = MockStudent.objects.get(registro=registro_estudiante)
            
            # Intención: Deuda
            if any(w in user_msg_lower for w in ["deuda", "monto", "pagar"]):
                financial = MockFinancialStatus.objects.filter(student=estudiante).last()
                if financial and financial.tiene_deuda:
                    return f"Hola {estudiante.nombre_completo}, tienes una deuda pendiente de **{financial.monto_deuda} Bs**.", 0
                else:
                    return f"Hola {estudiante.nombre_completo}, ¡no tienes deudas pendientes! 🎉", 0
            
            # Intención: Notas
            notas = MockAcademicRecord.objects.filter(student=estudiante)
            if not notas.exists():
                return f"Hola {estudiante.nombre_completo}, no encontré registros académicos asociados.", 0
            
            texto_notas = "\n".join([f"- **{n.materia}**: {n.nota} ({n.semestre})" for n in notas])
            return f"Hola {estudiante.nombre_completo}, aquí están tus notas registradas:\n\n{texto_notas}", 0
            
        except MockStudent.DoesNotExist:
            return "Error: Tu registro vinculado no existe en el sistema de la universidad.", 0
        except Exception as e:
            return f"Error al obtener datos académicos: {e}", 0

    # 5. RAG (Público) (y Privado con Permisos)
    # Definimos el rol para la búsqueda vectorial
    rol_actual = 'public'
    if usuario_autenticado:
        rol_actual = 'student'
        
    institutional_context = search_knowledge_base(mensaje_usuario, user_role=rol_actual)
    
    # Si no hay contexto y tampoco era un comando conocido, a veces conviene avisar
    if not institutional_context:
        # Opcional: Failover suave
        pass 

    final_context = (
        f"CONTEXTO PROPORCIONADO:\n{institutional_context}\n"
        f"--------------------------------------------------\n"
        f"INSTRUCCIONES:\n"
        f"Eres un asistente oficial de la UAGRM. Responde basándote estrictamente en el contexto. "
        f"Si la pregunta es sobre 'cerrar sesión' o temas técnicos del bot y no está en el contexto, responde genéricamente cómo usar el bot."
    )

    return get_openai_response(mensaje_usuario, final_context)