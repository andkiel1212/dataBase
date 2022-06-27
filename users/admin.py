from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser




@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('first_name', 'is_staff', 'is_active','email','image_tag')
    list_filter = ('email', 'is_staff', 'is_active',)
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name','image_tag')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
