from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = [
            'id', 'telegram_id', 'telegram_username', 'telegram_first_name', 
            'telegram_last_name', 'full_name', 'display_name', 'language',
            'exclude_passed_tickets', 'avatar', 'phone', 'is_verified',
            'is_active', 'created_at', 'last_activity'
        ]
        read_only_fields = [
            'id', 'telegram_id', 'telegram_username', 'telegram_first_name',
            'telegram_last_name', 'is_verified', 'is_active', 'created_at',
            'last_activity'
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ['language', 'exclude_passed_tickets', 'avatar', 'phone']
    
    def validate_language(self, value):
        """Validate language choice."""
        valid_languages = ['hy', 'ru', 'en']
        if value not in valid_languages:
            raise serializers.ValidationError(f"Language must be one of: {', '.join(valid_languages)}")
        return value


class UserStatsSerializer(serializers.ModelSerializer):
    """Serializer for user statistics."""
    
    statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'display_name', 'language', 'created_at', 'last_activity',
            'statistics'
        ]
    
    def get_statistics(self, obj):
        """Get user statistics."""
        if hasattr(obj, 'statistics'):
            stats = obj.statistics
            return {
                'total_attempts': stats.total_attempts,
                'total_questions_answered': stats.total_questions_answered,
                'total_correct_answers': stats.total_correct_answers,
                'average_score': stats.average_score,
                'completed_tickets_count': stats.completed_tickets_count,
                'total_time_formatted': stats.total_time_formatted,
                'last_attempt_at': stats.last_attempt_at,
            }
        return None

