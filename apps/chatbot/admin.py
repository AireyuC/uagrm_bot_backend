from django.contrib import admin
from .models import ChatHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'timestamp', 'tokens_used')
    list_filter = ('timestamp',)
    readonly_fields = ('session_id', 'user_message', 'bot_response', 'timestamp', 'tokens_used')
