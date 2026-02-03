from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import MockStudent, MockAcademicRecord, MockFinancialStatus
import uuid

class MockLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        registro = request.data.get('registro')
        password = request.data.get('password')

        try:
            student = MockStudent.objects.get(registro=registro, password=password)
            # Retorna un token falso simulado
            return Response({
                'token': f'mock-token-{uuid.uuid4()}',
                'nombre': student.nombre_completo
            }, status=status.HTTP_200_OK)
        except MockStudent.DoesNotExist:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

class MockGradesView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        registro = request.query_params.get('registro')
        if not registro:
             # Try to get from body if not in params, though GET usually uses params
             registro = request.data.get('registro')
        
        if not registro:
             return Response({'error': 'Registro requerido'}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(MockStudent, registro=registro)
        records = student.academic_records.all()
        
        data = [
            {
                'materia': r.materia,
                'nota': r.nota,
                'semestre': r.semestre
            }
            for r in records
        ]
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Support POST if needed by the specific integration architecture
        return self.get(request)

class MockDebtView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        registro = request.query_params.get('registro')
        if not registro:
             registro = request.data.get('registro')

        if not registro:
             return Response({'error': 'Registro requerido'}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(MockStudent, registro=registro)
        # Assuming one status record per student usually, or filter last
        financial = student.financial_status.last()
        
        if financial:
            return Response({
                'tiene_deuda': financial.tiene_deuda,
                'monto_deuda': financial.monto_deuda
            }, status=status.HTTP_200_OK)
        else:
             # Default state if no record exists
             return Response({
                'tiene_deuda': False,
                'monto_deuda': 0.00
            }, status=status.HTTP_200_OK)

    def post(self, request):
        return self.get(request)
