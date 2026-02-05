from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import StudentLoginForm
from .models import StudentConnection
# IMPORTANTE: Importamos el modelo de la simulación
from apps.simulation.models import MockStudent 

class LinkStudentView(View):
    def get(self, request):
        phone = request.GET.get('phone')
        if not phone:
            return render(request, 'chatbot/error.html', {'message': 'Falta el número de teléfono.'})
        
        form = StudentLoginForm(initial={'phone': phone})
        return render(request, 'chatbot/link_student.html', {'form': form, 'phone': phone})

    def post(self, request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            registro_input = form.cleaned_data['registro']
            password_input = form.cleaned_data['password']
            phone_input = form.cleaned_data['phone']

            # --- LÓGICA REALISTA ---
            # Buscamos directamente en la tabla de la "Universidad Simulada"
            try:
                # Verificamos si existe un estudiante con ese registro y password
                student = MockStudent.objects.get(registro=registro_input, password=password_input)
                
                # ¡SI EXISTE! -> Procedemos a vincular
                # Guardamos o actualizamos la conexión en la app del Chatbot
                StudentConnection.objects.update_or_create(
                    phone_number=phone_input,
                    defaults={
                        'student_id': student.registro, 
                        'is_active': True
                    }
                )
                
                # Renderizamos éxito pasando el nombre real del alumno
                return render(request, 'chatbot/success.html', {'student_name': student.nombre_completo})

            except MockStudent.DoesNotExist:
                # Si no lo encuentra o la clave está mal
                messages.error(request, "Credenciales incorrectas. Verifica tu Registro y Contraseña.")
        
        return render(request, 'chatbot/link_student.html', {'form': form})