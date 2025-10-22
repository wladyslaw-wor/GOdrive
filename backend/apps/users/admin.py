from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = [
        'telegram_id', 'display_name', 'telegram_username', 
        'language', 'is_active', 'is_admin', 'created_at', 'last_activity'
    ]
    list_filter = ['is_active', 'is_admin', 'is_verified', 'language', 'created_at']
    search_fields = ['telegram_id', 'telegram_username', 'telegram_first_name', 'telegram_last_name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Telegram Info', {
            'fields': ('telegram_id', 'telegram_username', 'telegram_first_name', 'telegram_last_name')
        }),
        ('Profile', {
            'fields': ('avatar', 'phone', 'language', 'exclude_passed_tickets')
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified', 'is_admin')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_activity'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['telegram_id', 'created_at', 'updated_at', 'last_activity']
    
    def has_add_permission(self, request):
        """Disable adding users through admin (they should be created via Telegram)."""
        return False

