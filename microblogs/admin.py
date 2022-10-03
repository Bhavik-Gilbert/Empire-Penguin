"""Configuration of the admin interface of microblogs."""
from django.contrib import admin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of tge admin interface for users"""
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active'
    ] 