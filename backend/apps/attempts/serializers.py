from rest_framework import serializers
from .models import Attempt, AttemptAnswer, UserStatistics
from apps.tickets.serializers import TicketListSerializer


class AttemptAnswerSerializer(serializers.ModelSerializer):
    """Serializer for attempt answers."""
    
    question_id = serializers.IntegerField(source='question.id')
    selected_option_id = serializers.IntegerField(source='selected_option.id')
    selected_option_text = serializers.CharField(source='selected_option.text', read_only=True)
    correct_option_id = serializers.SerializerMethodField()
    correct_option_text = serializers.SerializerMethodField()
    
    class Meta:
        model = AttemptAnswer
        fields = [
            'id', 'question_id', 'selected_option_id', 'selected_option_text',
            'correct_option_id', 'correct_option_text', 'is_correct',
            'time_spent_seconds', 'answered_at'
        ]
        read_only_fields = ['id', 'answered_at']
    
    def get_correct_option_id(self, obj):
        """Get correct option ID."""
        try:
            correct_option = obj.question.options.filter(is_correct=True).first()
            return correct_option.id if correct_option else None
        except:
            return None
    
    def get_correct_option_text(self, obj):
        """Get correct option text."""
        try:
            correct_option = obj.question.options.filter(is_correct=True).first()
            return correct_option.text if correct_option else None
        except:
            return None


class AttemptSerializer(serializers.ModelSerializer):
    """Serializer for attempts."""
    
    ticket = TicketListSerializer(read_only=True)
    answers = AttemptAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Attempt
        fields = [
            'id', 'ticket', 'mode', 'status', 'total_questions',
            'correct_answers', 'score_percentage', 'is_passed',
            'started_at', 'completed_at', 'duration_seconds', 'answers'
        ]
        read_only_fields = ['id', 'started_at', 'completed_at', 'duration_seconds']


class CreateAttemptSerializer(serializers.ModelSerializer):
    """Serializer for creating attempts."""
    
    class Meta:
        model = Attempt
        fields = ['ticket', 'mode']
    
    def create(self, validated_data):
        """Create attempt with user from context."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SubmitAnswerSerializer(serializers.Serializer):
    """Serializer for submitting answers."""
    
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField()
    time_spent_seconds = serializers.IntegerField(default=0)


class UserStatisticsSerializer(serializers.ModelSerializer):
    """Serializer for user statistics."""
    
    class Meta:
        model = UserStatistics
        fields = [
            'total_attempts', 'total_questions_answered', 'total_correct_answers',
            'average_score', 'completed_tickets_count', 'total_time_spent_seconds',
            'average_time_per_question', 'last_attempt_at', 'accuracy_percentage',
            'total_time_formatted'
        ]
        read_only_fields = '__all__'

