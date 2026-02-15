from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from apps.institutional.models import UploadedDocument
from apps.institutional.services.ingestion import process_pdf
from .serializers import DocumentUploadSerializer, DocumentSerializer, DocumentVerificationSerializer

class IsUploaderOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.groups.filter(name__in=['Uploader', 'Admin']).exists()
        )

class IsVerifierOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.groups.filter(name__in=['Verifier', 'Admin']).exists()
        )

class DocumentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        user = self.request.user
        # Admin/Verifier see all
        if user.is_staff or user.groups.filter(name__in=['Verifier', 'Admin']).exists():
            status = self.request.query_params.get('status')
            queryset = UploadedDocument.objects.all().order_by('-uploaded_at')
            if status:
                queryset = queryset.filter(status=status)
            return queryset
        
        # Uploader sees only their own
        return UploadedDocument.objects.filter(uploaded_by=user).order_by('-uploaded_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DocumentUploadSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user, status='PENDING')

class DocumentVerifyView(APIView):
    permission_classes = [IsVerifierOrAdmin]

    def post(self, request, pk):
        try:
            document = UploadedDocument.objects.get(pk=pk)
        except UploadedDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DocumentVerificationSerializer(document, data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            document.status = new_status
            document.save()
            
            # TRIGGER INGESTION IF APPROVED
            if new_status == 'APPROVED':
                # Run ingestion via celery in production, but here we can try synchronous or thread
                # For simplicity in prototype: Call directly (might block a bit)
                try:
                    process_pdf(document.id)
                except Exception as e:
                    return Response({
                        'warning': 'Document approved but ingestion failed',
                        'error': str(e)
                    }, status=status.HTTP_202_ACCEPTED)

            return Response(DocumentSerializer(document, context={'request': request}).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
