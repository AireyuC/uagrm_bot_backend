from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.academic.models import AcademicProfile
from .models import ChatHistory
from .services.ai_handler import get_openai_response
from .services.knowledge_retriever import search_knowledge_base

class ChatBotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_message = request.data.get('message')

        if not user_message:
            return Response({"error": "No se proporcionó mensaje"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Recuperar contexto acadmico (Privado)
        try:
            profile = user.academic_profile
            grades_context = "NOTAS DEL ESTUDIANTE (PRIVADO):\n"
            for grade_obj in profile.grades.all():
                grades_context += f"Periodo {grade_obj.periodo}: {grade_obj.data}\n"
            
            academic_context = f"Estudiante: {user.first_name} {user.last_name}\nCarrera: {profile.carrera}\n{grades_context}"
        except Exception:
            academic_context = f"Usuario: {user.username} (Sin perfil académico registrado)"

        # 2. Recuperar contexto institucional (Público/RAG)
        institutional_context = search_knowledge_base(user_message)

        # 3. Combinar Contextos
        final_context = (
            f"{academic_context}\n"
            f"--------------------------------------------------\n"
            f"{institutional_context}"
        )

        # 4. Llamar a OpenAI
        bot_reply, tokens = get_openai_response(user_message, final_context)

        # 5. Guardar historial
        ChatHistory.objects.create(
            user=user,
            user_message=user_message,
            bot_response=bot_reply,
            tokens_used=tokens
        )

        return Response({
            "response": bot_reply,
            "tokens": tokens
        })
