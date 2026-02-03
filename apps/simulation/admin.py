from django.contrib import admin
from .models import MockStudent, MockAcademicRecord, MockFinancialStatus

@admin.register(MockStudent)
class MockStudentAdmin(admin.ModelAdmin):
    list_display = ('registro', 'nombre_completo', 'carrera')
    search_fields = ('registro', 'nombre_completo')

@admin.register(MockAcademicRecord)
class MockAcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'materia', 'nota', 'semestre')
    list_filter = ('semestre', 'materia')
    search_fields = ('student__registro',)

@admin.register(MockFinancialStatus)
class MockFinancialStatusAdmin(admin.ModelAdmin):
    list_display = ('student', 'tiene_deuda', 'monto_deuda')
    list_filter = ('tiene_deuda',)
    search_fields = ('student__registro',)
