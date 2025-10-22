from rest_framework import serializers
from .models import Ticket, Question, AnswerOption, TicketCategory, UserTicketProgress


class AnswerOptionSerializer(serializers.ModelSerializer):
    """Serializer for answer options."""
    
    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'image', 'option_type', 'order']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions."""
    
    options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'image', 'explanation', 'explanation_image',
            'tags', 'difficulty_level', 'order', 'options'
        ]
        read_only_fields = ['id']


class TicketCategorySerializer(serializers.ModelSerializer):
    """Serializer for ticket categories."""
    
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description', 'order']
        read_only_fields = ['id']


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for tickets."""
    
    category = TicketCategorySerializer(read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    questions_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'number', 'title', 'description', 'category',
            'status', 'order', 'questions_count', 'questions',
            'created_at', 'published_at'
        ]
        read_only_fields = ['id', 'questions_count', 'created_at', 'published_at']


class TicketListSerializer(serializers.ModelSerializer):
    """Serializer for ticket list (without questions)."""
    
    category = TicketCategorySerializer(read_only=True)
    questions_count = serializers.ReadOnlyField()
    user_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'number', 'title', 'description', 'category',
            'status', 'order', 'questions_count', 'user_progress',
            'created_at', 'published_at'
        ]
        read_only_fields = ['id', 'questions_count', 'created_at', 'published_at']
    
    def get_user_progress(self, obj):
        """Get user progress for this ticket."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                progress = obj.user_progress.get(user=request.user)
                return {
                    'is_completed': progress.is_completed,
                    'completed_at': progress.completed_at,
                    'attempts_count': progress.attempts_count,
                    'best_score': progress.best_score,
                }
            except UserTicketProgress.DoesNotExist:
                return {
                    'is_completed': False,
                    'completed_at': None,
                    'attempts_count': 0,
                    'best_score': 0,
                }
        return None


class UserTicketProgressSerializer(serializers.ModelSerializer):
    """Serializer for user ticket progress."""
    
    ticket = TicketListSerializer(read_only=True)
    
    class Meta:
        model = UserTicketProgress
        fields = [
            'id', 'ticket', 'is_completed', 'completed_at',
            'attempts_count', 'best_score', 'total_questions_answered',
            'correct_answers_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuestionWithAnswerSerializer(serializers.ModelSerializer):
    """Serializer for questions with answer options (for testing)."""
    
    options = AnswerOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'image', 'order', 'options'
        ]
        read_only_fields = ['id']


class TicketForTestingSerializer(serializers.ModelSerializer):
    """Serializer for tickets in testing mode."""
    
    questions = QuestionWithAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'number', 'title', 'questions'
        ]
        read_only_fields = ['id']

