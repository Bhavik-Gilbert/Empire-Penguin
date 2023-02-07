"""Configuration of the admin interface of microblogs."""
from django.contrib import admin

from .models import User, Post

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active'
    ]


admin.site.register(Post)

# Superuser
"""
Admin
admin@example.com
Password
"""
