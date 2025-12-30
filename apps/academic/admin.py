from django.contrib import admin
from .models import AcademicProfile, MockGrades

class MockGradesInline(admin.TabularInline):
    model = MockGrades
    extra = 1

@admin.register(AcademicProfile)
class AcademicProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'carrera', 'semestre_actual')
    search_fields = ('user__username', 'carrera')
    inlines = [MockGradesInline]

@admin.register(MockGrades)
class MockGradesAdmin(admin.ModelAdmin):
    list_display = ('profile', 'periodo')
    list_filter = ('periodo',)
