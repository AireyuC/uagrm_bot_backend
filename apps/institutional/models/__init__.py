from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from pgvector.django import VectorField, HnswIndex

class UploadedDocument(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('REJECTED', 'Rechazado'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Documento_Subido'
        verbose_name_plural = 'Documentos_Subidos'
        db_table = 'institucional_documentos'

    def __str__(self):
        return self.title

class DocumentChunk(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=1536) # text-embedding-3-small

    class Meta:
        verbose_name = 'Fragmento_de_Documento'
        verbose_name_plural = 'Fragmentos_de_Documentos'
        db_table = 'institucional_fragmentos'
        indexes = [
            HnswIndex(
                name='chunk_embedding_idx',
                fields=['embedding'],
                opclasses=['vector_cosine_ops']
            )
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"

@receiver(models.signals.post_delete, sender=UploadedDocument)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Borra el archivo físico del sistema cuando se elimina el registro de la DB.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            try:
                os.remove(instance.file.path)
                print(f"Archivo físico eliminado: {instance.file.path}")
            except Exception as e:
                print(f"Error eliminando archivo físico: {e}")
