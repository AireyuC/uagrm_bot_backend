from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.academic.models import AcademicProfile
from .models import ChatHistory
from .services.ai_handler import get_openai_response
from .services.knowledge_retriever import search_knowledge_base

User = get_user_model()

class ChatBotView(APIView):
    permission_classes = [AllowAny] # Nivel global abierto, control manual en el código

    def post(self, request):
        user_message = request.data.get('message')
        phone_msg = request.data.get('phone') # Para WhatsApp/n8n
        
        if not user_message:
            return Response({"error": "No se proporcionó mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        # -------------------------------------------------------------
        # 1. JERARQUÍA DE IDENTIFICACIÓN DE USUARIO
        # -------------------------------------------------------------
        current_user = None # Default: Invitado
        auth_method = "INVITADO"

        # NIVEL 1: Token (App Móvil / Web Logueada)
        if request.user and request.user.is_authenticated:
            current_user = request.user
            auth_method = "TOKEN"
        
        # NIVEL 2: Teléfono (WhatsApp / n8n) - Solo si no hay Token
        elif phone_msg:
            try:
                current_user = User.objects.get(phone_number=phone_msg)
                auth_method = "TELEFONO"
            except User.DoesNotExist:
                 current_user = None # El número no está registrado, sigue como Invitado

        # -------------------------------------------------------------
        # 2. GENERACIÓN DE CONTEXTO (RAG)
        # -------------------------------------------------------------
        academic_context = ""
        
        # A) Contexto Académico (Solo si hay usuario identificado)
        if current_user:
            try:
                profile = current_user.academic_profile
                grades_str = "NOTAS DEL ESTUDIANTE (PRIVADO):\n"
                for grade_obj in profile.grades.all():
                    grades_str += f"- Periodo {grade_obj.periodo}: {grade_obj.data}\n"
                
                academic_context = (
                    f"CONTEXTO USUARIO ({auth_method}):\n"
                    f"Nombre: {current_user.first_name} {current_user.last_name}\n"
                    f"Carrera: {profile.carrera}\n"
                    f"{grades_str}\n"
                )
            except Exception:
                academic_context = f"CONTEXTO USUARIO ({auth_method}):\nUsuario registrado: {current_user.username} (Sin perfil académico)\n"
        else:
            academic_context = "CONTEXTO USUARIO: Invitado Anónimo (No dar información académica privada)."

        # B) Contexto Institucional (Para todos)
        institutional_context = search_knowledge_base(user_message)

        # C) Contexto Final Combinado
        final_context = (
            f"{academic_context}\n"
            f"--------------------------------------------------\n"
            f"{institutional_context}\n"
            f"--------------------------------------------------\n"
            f"INSTRUCCIONES ADICIONALES:\n"
            f"Si el usuario es Invitado, NO inventes notas ni datos privados. "
            f"Responde amablemente preguntas institucionales. "
            f"Si preguntan por sus notas y son invitados, diles que deben registrar su teléfono o loguearse."
        )

        # -------------------------------------------------------------
        # 3. LLAMADA A LA IA
        # -------------------------------------------------------------
        bot_reply, tokens = get_openai_response(user_message, final_context)

        # -------------------------------------------------------------
        # 4. GUARDAR HISTORIAL
        # -------------------------------------------------------------
        if current_user:
            ChatHistory.objects.create(
                user=current_user,
                user_message=user_message,
                bot_response=bot_reply,
                tokens_used=tokens
            )
        
        # NOTA: Si ChatHistory.user no acepta null, tendremos un error con invitados.
        # Por seguridad y consistencia con "No borrar nada anterior", asumiremos que los invitados
        # NO guardan historial o lo guardan con un usuario "anonymous" si se requiriera.
        # Pero para cumplir la tarea sin romper migraciones pasadas, pasaremos user=None
        # Si el modelo original tiene null=False, fallará. 
        # Revisemos modelos antiguos... "user = models.ForeignKey(User...)" suele ser null=False por defecto.
        # Haremos un try/catch o un workaround si falla, pero el código original de ChatHistory
        # probablemente requiera User. Vamos a arriesgarnos a pasar None?
        # Mejor: Si es None, no guardamos historial o usamos un usuario dummy?
        # Revisando el modelo ChatHistory en mi memoria: "user = ForeignKey(CustomUser, on_delete=CASCADE)"
        # Si no tiene null=True, fallará. 
        # SOLUCIÓN RÁPIDA: Solo guardar historial si current_user existe.

        return Response({
            "response": bot_reply,
            "tokens": tokens,
            "auth_method": auth_method
        })
