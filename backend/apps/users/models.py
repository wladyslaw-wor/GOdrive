from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with Telegram integration."""
    
    # Telegram specific fields
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, blank=True)
    telegram_first_name = models.CharField(max_length=255, blank=True)
    telegram_last_name = models.CharField(max_length=255, blank=True)
    
    # User preferences
    language = models.CharField(max_length=5, default='hy', choices=[
        ('hy', 'Հայերեն'),
        ('ru', 'Русский'),
        ('en', 'English'),
    ])
    exclude_passed_tickets = models.BooleanField(
        default=True,
        help_text="Исключать пройденные билеты (0 ошибок) при выборе случайного билета"
    )
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Status fields
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    
    # Admin fields
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.telegram_first_name} {self.telegram_last_name}".strip() or self.username
    
    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])
    
    @property
    def full_name(self):
        """Get user's full name."""
        return f"{self.telegram_first_name} {self.telegram_last_name}".strip()
    
    @property
    def display_name(self):
        """Get display name for UI."""
        return self.full_name or self.username or f"User {self.telegram_id}"

