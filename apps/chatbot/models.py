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
