from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model


from apps.chatbot.models import ChatHistory
from apps.chatbot.services.ai_handler import get_openai_response
from apps.chatbot.services.knowledge_retriever import search_knowledge_base

User = get_user_model()

class ChatBotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message')
        phone_msg = request.data.get('phone')

        if not user_message:
            return Response({"error": "No se proporcionó mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Identificación de Usuario (Solo para historial)
        current_user = None
        auth_method = "INVITADO"

        if request.user and request.user.is_authenticated:
            current_user = request.user
            auth_method = "TOKEN"
        elif phone_msg:
            try:
                current_user = User.objects.get(phone_number=phone_msg)
                auth_method = "TELEFONO"
            except User.DoesNotExist:
                 current_user = None

        # 2. Búsqueda de Información (Knowledege Base)
        institutional_context = search_knowledge_base(user_message)

        # 3. Construcción del Prompt (Rol: Asistente Oficial UAGRM)
        final_context = (
            f"CONTEXTO PROPORCIONADO:\n"
            f"{institutional_context}\n"
            f"--------------------------------------------------\n"
            f"INSTRUCCIONES:\n"
            f"Eres un asistente oficial de la UAGRM. Tu única fuente de verdad es el contexto proporcionado (reglamentos, fechas, trámites). "
            f"Si la información no está en el contexto, responde amablemente que no tienes esa información oficial y sugiere contactar a la universidad. "
            f"NO inventes datos."
        )

        # 4. Generación de Respuesta (OpenAI)
        bot_reply, tokens = get_openai_response(user_message, final_context)

        # 5. Registro de Historial
        if current_user:
            ChatHistory.objects.create(
                user=current_user,
                user_message=user_message,
                bot_response=bot_reply,
                tokens_used=tokens
            )

        return Response({
            "response": bot_reply,
            "tokens": tokens,
            "auth_method": auth_method
        })
