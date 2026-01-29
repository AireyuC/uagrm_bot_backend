from django.db import models
from pgvector.django import VectorField, HnswIndex

class UploadedDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

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
