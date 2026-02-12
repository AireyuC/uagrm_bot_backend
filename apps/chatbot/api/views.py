from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.chatbot.models import ChatHistory
from apps.chatbot.services.ai_handler import procesar_mensaje

class ChatBotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_message = request.data.get('message')
        phone_msg = request.data.get('phone') # Identificador opcional

        if not user_message:
            return Response({"error": "No se proporcionó mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Identificación de Sesión (Pública / Teléfono)
        session_id = phone_msg if phone_msg else "anonymous"

        # 2. Procesamiento Centralizado (RAG Público)
        bot_reply, tokens = procesar_mensaje(session_id, user_message)

        # 3. Registro de Historial
        ChatHistory.objects.create(
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_reply,
            tokens_used=tokens
        )

        return Response({
            "response": bot_reply,
            "tokens": tokens,
            "session_id": session_id
        })
