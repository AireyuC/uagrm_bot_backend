from django.db import models
from django.conf import settings

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_history')
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tokens_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Chat de {self.user.username} - {self.timestamp}"

class StudentConnection(models.Model):
    """
    [DEPRECATED] Modelo DEPRECATED. No se usa en la versión actual pública.
    Diseñado originalmente para vincular cuentas de WhatsApp con registros de estudiantes.
    """
    phone_number = models.CharField(max_length=20, unique=True, help_text="Número de WhatsApp")
    student_id = models.CharField(max_length=20, help_text="Registro Universitario")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone_number} -> {self.student_id}"
