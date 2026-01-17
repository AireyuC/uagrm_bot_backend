from django.contrib import admin
from .models import ChatHistory

# @admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'tokens_used')
    list_filter = ('timestamp',)
    readonly_fields = ('user', 'user_message', 'bot_response', 'timestamp', 'tokens_used')
