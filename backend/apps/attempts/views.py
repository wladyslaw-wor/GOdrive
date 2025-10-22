from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Attempt, AttemptAnswer, UserStatistics
from .serializers import (
    AttemptSerializer, CreateAttemptSerializer, SubmitAnswerSerializer,
    UserStatisticsSerializer
)
from apps.users.authentication import TelegramAuthentication
from apps.tickets.models import Ticket, Question, AnswerOption


class AttemptListView(generics.ListAPIView):
    """List user's attempts."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = AttemptSerializer
    
    def get_queryset(self):
        """Get user's attempts."""
        return Attempt.objects.filter(
            user=self.request.user
        ).prefetch_related('ticket', 'answers').order_by('-started_at')


class AttemptDetailView(generics.RetrieveAPIView):
    """Get attempt details."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = AttemptSerializer
    
    def get_queryset(self):
        """Get user's attempts."""
        return Attempt.objects.filter(
            user=self.request.user
        ).prefetch_related('ticket', 'answers__question', 'answers__selected_option')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_attempt(request):
    """Create new attempt."""
    serializer = CreateAttemptSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        ticket = serializer.validated_data['ticket']
        mode = serializer.validated_data['mode']
        
        # Check if ticket is published
        if ticket.status != 'published':
            return Response(
                {'error': 'Ticket is not published'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create attempt
        attempt = serializer.save()
        
        # Set total questions count
        attempt.total_questions = ticket.questions.filter(is_active=True).count()
        attempt.save()
        
        return Response(
            AttemptSerializer(attempt).data, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request, attempt_id):
    """Submit answer for question in attempt."""
    try:
        attempt = Attempt.objects.get(
            id=attempt_id,
            user=request.user,
            status='in_progress'
        )
    except Attempt.DoesNotExist:
        return Response(
            {'error': 'Attempt not found or not in progress'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = SubmitAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    question_id = serializer.validated_data['question_id']
    selected_option_id = serializer.validated_data['selected_option_id']
    time_spent = serializer.validated_data['time_spent_seconds']
    
    try:
        question = Question.objects.get(id=question_id, ticket=attempt.ticket)
        selected_option = AnswerOption.objects.get(id=selected_option_id, question=question)
    except (Question.DoesNotExist, AnswerOption.DoesNotExist):
        return Response(
            {'error': 'Question or option not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Check if answer already exists
    if AttemptAnswer.objects.filter(attempt=attempt, question=question).exists():
        return Response(
            {'error': 'Answer already submitted for this question'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if answer is correct
    is_correct = selected_option.is_correct
    
    # Create answer
    answer = AttemptAnswer.objects.create(
        attempt=attempt,
        question=question,
        selected_option=selected_option,
        is_correct=is_correct,
        time_spent_seconds=time_spent
    )
    
    # Update attempt counters
    attempt.correct_answers += 1 if is_correct else 0
    attempt.save()
    
    return Response({
        'is_correct': is_correct,
        'correct_option_id': question.options.filter(is_correct=True).first().id,
        'explanation': question.explanation if attempt.mode == 'learning' else None,
        'explanation_image': question.explanation_image.url if question.explanation_image and attempt.mode == 'learning' else None,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_attempt(request, attempt_id):
    """Complete attempt and calculate final results."""
    try:
        attempt = Attempt.objects.get(
            id=attempt_id,
            user=request.user,
            status='in_progress'
        )
    except Attempt.DoesNotExist:
        return Response(
            {'error': 'Attempt not found or not in progress'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Complete attempt
    attempt.complete()
    
    # Update user statistics
    user = request.user
    if hasattr(user, 'statistics'):
        user.statistics.update_statistics()
    else:
        UserStatistics.objects.create(user=user)
        user.statistics.update_statistics()
    
    return Response(AttemptSerializer(attempt).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_statistics(request):
    """Get user statistics."""
    user = request.user
    
    # Create statistics if not exists
    if not hasattr(user, 'statistics'):
        UserStatistics.objects.create(user=user)
    
    # Update statistics
    user.statistics.update_statistics()
    
    serializer = UserStatisticsSerializer(user.statistics)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attempt_review(request, attempt_id):
    """Get attempt review with all answers."""
    try:
        attempt = Attempt.objects.get(
            id=attempt_id,
            user=request.user,
            status='completed'
        )
    except Attempt.DoesNotExist:
        return Response(
            {'error': 'Completed attempt not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get all answers with explanations
    answers = AttemptAnswer.objects.filter(attempt=attempt).select_related(
        'question', 'selected_option'
    ).prefetch_related('question__options')
    
    review_data = []
    for answer in answers:
        correct_option = answer.question.options.filter(is_correct=True).first()
        review_data.append({
            'question_id': answer.question.id,
            'question_text': answer.question.text,
            'question_image': answer.question.image.url if answer.question.image else None,
            'selected_option_id': answer.selected_option.id,
            'selected_option_text': answer.selected_option.text,
            'correct_option_id': correct_option.id if correct_option else None,
            'correct_option_text': correct_option.text if correct_option else None,
            'is_correct': answer.is_correct,
            'explanation': answer.question.explanation,
            'explanation_image': answer.question.explanation_image.url if answer.question.explanation_image else None,
            'time_spent_seconds': answer.time_spent_seconds,
        })
    
    return Response({
        'attempt': AttemptSerializer(attempt).data,
        'review': review_data,
    })

