from django.db import models

class Documentos(models.Model):
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='documentos/')
    descripcion = models.TextField()

class KnowledgeBase(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Texto completo de la información (reglamentos, fechas, etc.)")
    keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Palabras clave separadas por comas")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
