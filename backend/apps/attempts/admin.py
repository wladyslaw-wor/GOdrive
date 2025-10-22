from django.contrib import admin
from .models import Attempt, AttemptAnswer, UserStatistics


class AttemptAnswerInline(admin.TabularInline):
    """Inline admin for attempt answers."""
    model = AttemptAnswer
    extra = 0
    fields = ['question', 'selected_option', 'is_correct', 'time_spent_seconds', 'answered_at']
    readonly_fields = ['answered_at']
    ordering = ['answered_at']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """Admin configuration for Attempt model."""
    
    list_display = [
        'user', 'ticket', 'mode', 'status', 'score_percentage',
        'is_passed', 'started_at', 'completed_at', 'duration_seconds'
    ]
    list_filter = ['mode', 'status', 'is_passed', 'started_at', 'completed_at']
    search_fields = ['user__display_name', 'ticket__number', 'ticket__title']
    ordering = ['-started_at']
    
    fieldsets = (
        ('Attempt Info', {
            'fields': ('user', 'ticket', 'mode', 'status')
        }),
        ('Results', {
            'fields': ('total_questions', 'correct_answers', 'score_percentage', 'is_passed')
        }),
        ('Timestamps', {
            'fields': ('started_at', 'completed_at', 'duration_seconds'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['started_at', 'completed_at', 'duration_seconds']
    
    inlines = [AttemptAnswerInline]


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    """Admin configuration for AttemptAnswer model."""
    
    list_display = [
        'attempt', 'question', 'selected_option', 'is_correct',
        'time_spent_seconds', 'answered_at'
    ]
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['attempt__user__display_name', 'question__text']
    ordering = ['-answered_at']
    
    fieldsets = (
        ('Answer', {
            'fields': ('attempt', 'question', 'selected_option', 'is_correct')
        }),
        ('Timing', {
            'fields': ('time_spent_seconds', 'answered_at')
        }),
    )
    
    readonly_fields = ['answered_at']


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    """Admin configuration for UserStatistics model."""
    
    list_display = [
        'user', 'total_attempts', 'total_questions_answered',
        'average_score', 'completed_tickets_count', 'last_attempt_at'
    ]
    list_filter = ['last_attempt_at']
    search_fields = ['user__display_name']
    ordering = ['-last_attempt_at']
    
    fieldsets = (
        ('Overall Statistics', {
            'fields': ('user', 'total_attempts', 'total_questions_answered', 'total_correct_answers')
        }),
        ('Performance', {
            'fields': ('average_score', 'completed_tickets_count')
        }),
        ('Time Statistics', {
            'fields': ('total_time_spent_seconds', 'average_time_per_question')
        }),
        ('Last Activity', {
            'fields': ('last_attempt_at',)
        }),
    )
    
    readonly_fields = '__all__'

