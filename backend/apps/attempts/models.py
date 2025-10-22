from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Attempt(models.Model):
    """Попытка прохождения тестирования."""
    
    MODE_CHOICES = [
        ('learning', 'Обучение'),
        ('testing', 'Тестирование'),
    ]
    
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('abandoned', 'Прервано'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts', verbose_name="Пользователь")
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='attempts', verbose_name="Билет")
    
    # Attempt details
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, verbose_name="Режим")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="Статус")
    
    # Results
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Всего вопросов")
    correct_answers = models.PositiveIntegerField(default=0, verbose_name="Правильных ответов")
    score_percentage = models.PositiveIntegerField(default=0, verbose_name="Процент правильных ответов")
    is_passed = models.BooleanField(default=False, verbose_name="Пройден")
    
    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начато")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершено")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name="Длительность (секунды)")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'attempts'
        verbose_name = 'Попытка тестирования'
        verbose_name_plural = 'Попытки тестирования'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.display_name} - {self.ticket.number} ({self.mode})"
    
    def complete(self):
        """Mark attempt as completed and calculate results."""
        self.status = 'completed'
        self.completed_at = timezone.now()
        
        if self.started_at:
            duration = self.completed_at - self.started_at
            self.duration_seconds = int(duration.total_seconds())
        
        # Calculate score
        if self.total_questions > 0:
            self.score_percentage = int((self.correct_answers / self.total_questions) * 100)
            self.is_passed = self.score_percentage == 100
        
        self.save()
        
        # Update user progress
        self.update_user_progress()
    
    def update_user_progress(self):
        """Update user's progress for this ticket."""
        from apps.tickets.models import UserTicketProgress
        
        progress, created = UserTicketProgress.objects.get_or_create(
            user=self.user,
            ticket=self.ticket
        )
        progress.update_progress(self.correct_answers, self.total_questions)


class AttemptAnswer(models.Model):
    """Ответ пользователя на вопрос в попытке."""
    
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='answers', verbose_name="Попытка")
    question = models.ForeignKey('tickets.Question', on_delete=models.CASCADE, verbose_name="Вопрос")
    selected_option = models.ForeignKey(
        'tickets.AnswerOption', 
        on_delete=models.CASCADE, 
        verbose_name="Выбранный вариант"
    )
    is_correct = models.BooleanField(verbose_name="Правильный ответ")
    time_spent_seconds = models.PositiveIntegerField(default=0, verbose_name="Время на ответ (секунды)")
    
    # Timestamps
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Ответ дан")
    
    class Meta:
        db_table = 'attempt_answers'
        verbose_name = 'Ответ в попытке'
        verbose_name_plural = 'Ответы в попытках'
        unique_together = ['attempt', 'question']
        ordering = ['answered_at']
    
    def __str__(self):
        return f"{self.attempt} - {self.question.ticket.number} Q{self.question.order}"


class UserStatistics(models.Model):
    """Агрегированная статистика пользователя."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics', verbose_name="Пользователь")
    
    # Overall statistics
    total_attempts = models.PositiveIntegerField(default=0, verbose_name="Всего попыток")
    total_questions_answered = models.PositiveIntegerField(default=0, verbose_name="Всего отвечено вопросов")
    total_correct_answers = models.PositiveIntegerField(default=0, verbose_name="Всего правильных ответов")
    average_score = models.FloatField(default=0.0, verbose_name="Средний балл")
    
    # Completed tickets
    completed_tickets_count = models.PositiveIntegerField(default=0, verbose_name="Пройденных билетов")
    
    # Time statistics
    total_time_spent_seconds = models.PositiveIntegerField(default=0, verbose_name="Общее время (секунды)")
    average_time_per_question = models.FloatField(default=0.0, verbose_name="Среднее время на вопрос")
    
    # Last activity
    last_attempt_at = models.DateTimeField(null=True, blank=True, verbose_name="Последняя попытка")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_statistics'
        verbose_name = 'Статистика пользователя'
        verbose_name_plural = 'Статистика пользователей'
    
    def __str__(self):
        return f"Статистика {self.user.display_name}"
    
    def update_statistics(self):
        """Update user statistics based on all attempts."""
        attempts = self.user.attempts.filter(status='completed')
        
        self.total_attempts = attempts.count()
        self.total_questions_answered = sum(attempt.total_questions for attempt in attempts)
        self.total_correct_answers = sum(attempt.correct_answers for attempt in attempts)
        self.total_time_spent_seconds = sum(
            attempt.duration_seconds for attempt in attempts 
            if attempt.duration_seconds
        )
        
        # Calculate averages
        if self.total_questions_answered > 0:
            self.average_score = (self.total_correct_answers / self.total_questions_answered) * 100
            self.average_time_per_question = self.total_time_spent_seconds / self.total_questions_answered
        
        # Count completed tickets
        self.completed_tickets_count = self.user.ticket_progress.filter(is_completed=True).count()
        
        # Last attempt
        last_attempt = attempts.order_by('-started_at').first()
        if last_attempt:
            self.last_attempt_at = last_attempt.started_at
        
        self.save()
    
    @property
    def accuracy_percentage(self):
        """Get accuracy percentage."""
        return self.average_score
    
    @property
    def total_time_formatted(self):
        """Get formatted total time."""
        hours = self.total_time_spent_seconds // 3600
        minutes = (self.total_time_spent_seconds % 3600) // 60
        return f"{hours}ч {minutes}м"

