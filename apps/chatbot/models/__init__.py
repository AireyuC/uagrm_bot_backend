from django.db import models
from django.conf import settings

class ChatHistory(models.Model):
    # Public mode: No user FK. Just storing request identifier (e.g. phone)
    session_id = models.CharField(max_length=100, null=True, blank=True, help_text="Identificador de sesión o teléfono")
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tokens_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Chat {self.session_id} - {self.timestamp}"


