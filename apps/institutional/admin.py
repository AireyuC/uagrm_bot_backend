from django.contrib import admin
from django.contrib import messages
from .models import UploadedDocument, DocumentChunk 
from .services.ingestion import process_pdf

def procesar_documentos(modeladmin, request, queryset):
    """Acción admin para procesar PDFs seleccionados y generar embeddings."""
    count = 0
    for doc in queryset:
        try:
            process_pdf(doc.id)
            count += 1
        except Exception as e:
            modeladmin.message_user(request, f"Error en {doc.title}: {e}", level=messages.ERROR)
    
    modeladmin.message_user(request, f"{count} documentos procesados correctamente.", level=messages.SUCCESS)

procesar_documentos.short_description = "Procesar PDF (Extraer Texto + Embeddings)"

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')
    actions = [procesar_documentos]

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index', 'preview_text')
    list_filter = ('document',)
    
    def preview_text(self, obj):
        return obj.chunk_text[:50] + "..."