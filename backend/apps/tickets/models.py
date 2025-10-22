from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class TicketCategory(models.Model):
    """Категория билетов (например, по темам ПДД)."""
    
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ticket_categories'
        verbose_name = 'Категория билетов'
        verbose_name_plural = 'Категории билетов'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Билет с вопросами."""
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архив'),
    ]
    
    number = models.CharField(max_length=50, unique=True, verbose_name="Номер билета")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(
        TicketCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Категория"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name="Статус"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    questions_count = models.PositiveIntegerField(default=0, verbose_name="Количество вопросов")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Создал")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tickets'
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'
        ordering = ['order', 'number']
    
    def __str__(self):
        return f"{self.number}: {self.title}"
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
        self.update_questions_count()
    
    def update_questions_count(self):
        """Update questions count for this ticket."""
        count = self.questions.filter(is_active=True).count()
        if count != self.questions_count:
            self.questions_count = count
            self.save(update_fields=['questions_count'])


class Question(models.Model):
    """Вопрос в билете."""
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='questions', verbose_name="Билет")
    text = models.TextField(verbose_name="Текст вопроса")
    image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name="Изображение")
    explanation = models.TextField(blank=True, verbose_name="Объяснение")
    explanation_image = models.ImageField(upload_to='explanations/', blank=True, null=True, verbose_name="Изображение в объяснении")
    
    # Question metadata
    tags = models.CharField(max_length=500, blank=True, verbose_name="Теги (через запятую)")
    difficulty_level = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Уровень сложности"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок в билете")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Создал")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['ticket', 'order']
        unique_together = ['ticket', 'order']
    
    def __str__(self):
        return f"{self.ticket.number}: {self.text[:50]}..."


class AnswerOption(models.Model):
    """Вариант ответа на вопрос."""
    
    OPTION_TYPES = [
        ('text', 'Текст'),
        ('image', 'Изображение'),
    ]
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', verbose_name="Вопрос")
    text = models.CharField(max_length=1000, blank=True, verbose_name="Текст варианта")
    image = models.ImageField(upload_to='answer_options/', blank=True, null=True, verbose_name="Изображение варианта")
    option_type = models.CharField(max_length=10, choices=OPTION_TYPES, default='text', verbose_name="Тип варианта")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    order = models.PositiveIntegerField(verbose_name="Порядок")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'answer_options'
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
    
    def __str__(self):
        option_text = self.text[:30] if self.text else f"Изображение {self.order}"
        return f"{self.question.ticket.number}: {option_text}"


class UserTicketProgress(models.Model):
    """Прогресс пользователя по билетам."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket_progress', verbose_name="Пользователь")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='user_progress', verbose_name="Билет")
    
    # Progress data
    is_completed = models.BooleanField(default=False, verbose_name="Пройден")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата прохождения")
    attempts_count = models.PositiveIntegerField(default=0, verbose_name="Количество попыток")
    best_score = models.PositiveIntegerField(default=0, verbose_name="Лучший результат")
    total_questions_answered = models.PositiveIntegerField(default=0, verbose_name="Всего отвечено вопросов")
    correct_answers_count = models.PositiveIntegerField(default=0, verbose_name="Правильных ответов")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_ticket_progress'
        verbose_name = 'Прогресс по билету'
        verbose_name_plural = 'Прогресс по билетам'
        unique_together = ['user', 'ticket']
    
    def __str__(self):
        return f"{self.user.display_name} - {self.ticket.number}"
    
    def update_progress(self, correct_answers, total_questions):
        """Update user progress for this ticket."""
        self.total_questions_answered += total_questions
        self.correct_answers_count += correct_answers
        self.attempts_count += 1
        
        # Calculate score percentage
        score = int((self.correct_answers_count / self.total_questions_answered) * 100) if self.total_questions_answered > 0 else 0
        self.best_score = max(self.best_score, score)
        
        # Mark as completed if 100% correct
        if score == 100 and not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
        
        self.save()

