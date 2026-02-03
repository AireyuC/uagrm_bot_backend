from django.db import models

class MockStudent(models.Model):
    registro = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)  # Plain text is ok for mock
    nombre_completo = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_completo} ({self.registro})"

class MockAcademicRecord(models.Model):
    student = models.ForeignKey(MockStudent, on_delete=models.CASCADE, related_name='academic_records')
    materia = models.CharField(max_length=100)
    nota = models.IntegerField()
    semestre = models.CharField(max_length=20)  # e.g., "1-2025"

    def __str__(self):
        return f"{self.materia}: {self.nota} - {self.student.registro}"

class MockFinancialStatus(models.Model):
    student = models.ForeignKey(MockStudent, on_delete=models.CASCADE, related_name='financial_status')
    tiene_deuda = models.BooleanField(default=False)
    monto_deuda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Deuda: {self.tiene_deuda} ({self.monto_deuda}) - {self.student.registro}"
