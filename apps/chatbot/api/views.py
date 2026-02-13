from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_api_key.permissions import HasAPIKey
from django.core.files.storage import default_storage
import os

from apps.chatbot.models import ChatHistory
from apps.chatbot.services.ai_handler import procesar_mensaje
from apps.institutional.models import UploadedDocument
from apps.institutional.services.ingestion import process_pdf

# Solo pasara quien tenga una ApiKey valida
class SecureUploadView(APIView):
    permission_classes = [HasAPIKey]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')
        
        if not uploaded_file:
            return Response(
                {"error": "No se envió ningún archivo."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # LISTA BLANCA DE EXTENSIONES PERMITIDAS
        ALLOWED_EXTENSIONS = ['.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
        
        # Obtener la extensión del archivo (ej: .docx)
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
             return Response(
                {"error": f"Formato no permitido. Solo aceptamos: {', '.join(ALLOWED_EXTENSIONS)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Guardar el archivo y crear registro en BD
        try:
            doc = UploadedDocument.objects.create(
                title=uploaded_file.name,
                file=uploaded_file
            )
            
            # Procesar el PDF inmediatamente (Extracción + Sanitización + Embeddings)
            # Aunque se procese, el status por defecto es 'PENDING', así que el RAG lo ignorará.
            try:
                process_pdf(doc.id)
                message = "Archivo recibido y procesado correctamente. Pendiente de aprobación."
            except Exception as e:
                # Si falla el procesamiento, el archivo sigue subido pero quizás sin chunks
                message = f"Archivo recibido, pero hubo un error en el pre-procesamiento: {str(e)}"

            return Response({
                "status": "success",
                "message": message,
                "file_type": ext,
                "document_id": doc.id,
                "document_status": doc.status
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error al guardar el documento: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
