from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ESTUDIANTE = 'ESTUDIANTE', 'Estudiante'
        DOCENTE = 'DOCENTE', 'Docente'
        ADMIN = 'ADMIN', 'Administrador'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ESTUDIANTE
    )
    student_code = models.CharField(max_length=20, blank=True, null=True, help_text="Código de registro estudiantil o docente")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
