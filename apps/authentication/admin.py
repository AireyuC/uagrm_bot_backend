from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    
    # Campos que aparecen al EDITAR un usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('role', 'student_code', 'phone_number')}),
    )
    
    # Campos que aparecen al CREAR un usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {'fields': ('role', 'student_code', 'phone_number')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
