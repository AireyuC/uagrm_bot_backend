from django.db import models
from pgvector.django import VectorField, HnswIndex

class Documentos(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField()

class UploadedDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DocumentChunk(models.Model):
    document = models.ForeignKey(UploadedDocument, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=1536) # text-embedding-3-small

    class Meta:
        indexes = [
            HnswIndex(
                name='chunk_embedding_idx',
                fields=['embedding'],
                opclasses=['vector_cosine_ops']
            )
        ]

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"

class KnowledgeBase(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Texto completo de la información (reglamentos, fechas, etc.)")
    keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Palabras clave separadas por comas")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
