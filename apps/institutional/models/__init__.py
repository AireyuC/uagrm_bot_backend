import os
from django.db import models
from django.dispatch import receiver
from pgvector.django import VectorField, HnswIndex

class UploadedDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    ACCESS_CHOICES = [
        ('public', 'Público (Todos)'),
        # [DEPRECATED-PUBLIC-MODE]
        # ('student', 'Solo Estudiantes'),
        # ('teacher', 'Solo Docentes'),
        # ('admin', 'Solo Administrativos'),
        # ('staff', 'Docentes y Administrativos'),
    ]
    access_level = models.CharField(
        max_length=20, 
        choices=ACCESS_CHOICES, 
        default='public',
        help_text="Quién puede ver este documento en el chat."
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
