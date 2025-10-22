import hmac
import hashlib
import json
import time
from urllib.parse import parse_qsl, unquote
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class TelegramAuthentication(BaseAuthentication):
    """Authentication class for Telegram WebApp initData."""
    
    def authenticate(self, request):
        init_data = request.META.get('HTTP_X_TELEGRAM_INIT_DATA')
        if not init_data:
            return None
        
        try:
            user = self.validate_telegram_data(init_data)
            return (user, None)
        except Exception:
            return None
    
    def validate_telegram_data(self, init_data):
        """Validate Telegram WebApp initData and return user."""
        # Parse init data
        parsed_data = dict(parse_qsl(init_data))
        
        # Extract hash and remove it from data
        received_hash = parsed_data.pop('hash', None)
        if not received_hash:
            raise AuthenticationFailed('No hash in init data')
        
        # Create data string for verification
        data_check_string = '\n'.join([
            f"{key}={value}" 
            for key, value in sorted(parsed_data.items())
        ])
        
        # Create secret key
        secret_key = hmac.new(
            b"WebAppData", 
            self.get_bot_token().encode(), 
            hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key, 
            data_check_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        # Verify hash
        if not hmac.compare_digest(received_hash, calculated_hash):
            raise AuthenticationFailed('Invalid hash')
        
        # Check auth_date (should be recent)
        auth_date = int(parsed_data.get('auth_date', 0))
        if time.time() - auth_date > 86400:  # 24 hours
            raise AuthenticationFailed('Init data expired')
        
        # Parse user data
        user_data = json.loads(parsed_data.get('user', '{}'))
        
        # Get or create user
        user = self.get_or_create_user(user_data)
        return user
    
    def get_bot_token(self):
        """Get bot token from settings."""
        from django.conf import settings
        return settings.TELEGRAM_BOT_TOKEN
    
    def get_or_create_user(self, user_data):
        """Get or create user from Telegram user data."""
        telegram_id = user_data.get('id')
        if not telegram_id:
            raise AuthenticationFailed('No user ID in init data')
        
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'telegram_username': user_data.get('username', ''),
                'telegram_first_name': user_data.get('first_name', ''),
                'telegram_last_name': user_data.get('last_name', ''),
                'username': f"tg_{telegram_id}",
                'is_active': True,
                'is_verified': True,
            }
        )
        
        # Update user data if changed
        if not created:
            updated = False
            if user.telegram_username != user_data.get('username', ''):
                user.telegram_username = user_data.get('username', '')
                updated = True
            if user.telegram_first_name != user_data.get('first_name', ''):
                user.telegram_first_name = user_data.get('first_name', '')
                updated = True
            if user.telegram_last_name != user_data.get('last_name', ''):
                user.telegram_last_name = user_data.get('last_name', '')
                updated = True
            
            if updated:
                user.save()
        
        # Update last activity
        user.update_activity()
        
        return user


class TelegramBackend(BaseBackend):
    """Django authentication backend for Telegram."""
    
    def authenticate(self, request, telegram_id=None, **kwargs):
        if not telegram_id:
            return None
        
        try:
            return User.objects.get(telegram_id=telegram_id, is_active=True)
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None

