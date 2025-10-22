from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Ticket, Question, UserTicketProgress
from .serializers import (
    TicketSerializer, TicketListSerializer, TicketForTestingSerializer,
    UserTicketProgressSerializer, QuestionSerializer
)
from apps.users.authentication import TelegramAuthentication


class TicketListView(generics.ListAPIView):
    """List all published tickets."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = TicketListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['number', 'title', 'description']
    ordering_fields = ['order', 'number', 'title', 'created_at']
    ordering = ['order', 'number']
    
    def get_queryset(self):
        """Get published tickets."""
        return Ticket.objects.filter(status='published').prefetch_related(
            'category', 'user_progress'
        )


class TicketDetailView(generics.RetrieveAPIView):
    """Get ticket details with questions (for learning mode)."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = TicketSerializer
    lookup_field = 'number'
    
    def get_queryset(self):
        """Get published tickets."""
        return Ticket.objects.filter(status='published').prefetch_related(
            'category', 'questions__options'
        )


class TicketForTestingView(generics.RetrieveAPIView):
    """Get ticket for testing mode (without explanations)."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = TicketForTestingSerializer
    lookup_field = 'number'
    
    def get_queryset(self):
        """Get published tickets."""
        return Ticket.objects.filter(status='published').prefetch_related(
            'questions__options'
        )


class UserProgressListView(generics.ListAPIView):
    """List user's progress on tickets."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = UserTicketProgressSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_completed']
    ordering_fields = ['created_at', 'updated_at', 'best_score', 'attempts_count']
    ordering = ['-updated_at']
    
    def get_queryset(self):
        """Get user's progress."""
        return UserTicketProgress.objects.filter(
            user=self.request.user
        ).prefetch_related('ticket')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_random_ticket(request):
    """Get random ticket for testing (excluding passed ones if setting enabled)."""
    user = request.user
    
    # Base queryset
    queryset = Ticket.objects.filter(status='published')
    
    # Exclude passed tickets if user setting is enabled
    if user.exclude_passed_tickets:
        passed_tickets = UserTicketProgress.objects.filter(
            user=user,
            is_completed=True
        ).values_list('ticket_id', flat=True)
        queryset = queryset.exclude(id__in=passed_tickets)
    
    # Get random ticket
    ticket = queryset.order_by('?').first()
    
    if not ticket:
        return Response(
            {'message': 'No available tickets'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = TicketForTestingSerializer(ticket)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question_explanation(request, question_id):
    """Get question explanation (for learning mode)."""
    try:
        question = Question.objects.get(
            id=question_id,
            ticket__status='published'
        )
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response(
            {'message': 'Question not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get user statistics."""
    user = request.user
    
    # Update statistics
    if hasattr(user, 'statistics'):
        user.statistics.update_statistics()
    
    stats = {
        'total_attempts': 0,
        'total_questions_answered': 0,
        'total_correct_answers': 0,
        'average_score': 0,
        'completed_tickets_count': 0,
        'total_time_spent_seconds': 0,
    }
    
    if hasattr(user, 'statistics'):
        stats.update({
            'total_attempts': user.statistics.total_attempts,
            'total_questions_answered': user.statistics.total_questions_answered,
            'total_correct_answers': user.statistics.total_correct_answers,
            'average_score': user.statistics.average_score,
            'completed_tickets_count': user.statistics.completed_tickets_count,
            'total_time_spent_seconds': user.statistics.total_time_spent_seconds,
            'total_time_formatted': user.statistics.total_time_formatted,
            'last_attempt_at': user.statistics.last_attempt_at,
        })
    
    return Response(stats)

