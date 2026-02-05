from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model


from apps.chatbot.models import ChatHistory
from apps.chatbot.services.ai_handler import procesar_mensaje
# from apps.chatbot.services.knowledge_retriever import search_knowledge_base # Ya no es necesario aquí

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

        # 2. Procesamiento Centralizado (Auth, Privacidad, RAG)
        bot_reply, tokens = procesar_mensaje(phone_msg, user_message)

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
