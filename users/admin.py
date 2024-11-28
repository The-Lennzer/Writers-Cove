# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser

class CustomUserAdmin(UserAdmin):
    model = NewUser
    list_display = ('email', 'user_name', 'first_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'user_name')
    ordering = ('email',)

admin.site.register(NewUser, CustomUserAdmin)
