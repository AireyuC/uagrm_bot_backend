from django.db import models
from django.conf import settings

class AcademicProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='academic_profile')
    carrera = models.CharField(max_length=100)
    semestre_actual = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Perfil de {self.user.username} - {self.carrera}"

class MockGrades(models.Model):
    profile = models.ForeignKey(AcademicProfile, on_delete=models.CASCADE, related_name='grades')
    periodo = models.CharField(max_length=20, default='2024-1')
    data = models.JSONField(default=dict, help_text="Formato: {'materia': nota, ...}")

    def __str__(self):
        return f"Notas {self.periodo} - {self.profile.user.username}"
