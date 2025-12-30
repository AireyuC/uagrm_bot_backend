from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Información Académica', {'fields': ('role', 'student_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Académica', {'fields': ('role', 'student_code')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
