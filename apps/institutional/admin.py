from django.contrib import admin
from .models import Documentos, KnowledgeBase

admin.site.register(Documentos)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'updated_at')
    search_fields = ('title', 'content', 'keywords')
    list_filter = ('is_active',)
