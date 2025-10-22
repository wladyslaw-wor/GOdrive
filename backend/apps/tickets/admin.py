from django.contrib import admin
from .models import TicketCategory, Ticket, Question, AnswerOption, UserTicketProgress


class AnswerOptionInline(admin.TabularInline):
    """Inline admin for answer options."""
    model = AnswerOption
    extra = 0
    fields = ['text', 'image', 'option_type', 'is_correct', 'order']
    ordering = ['order']


class QuestionInline(admin.TabularInline):
    """Inline admin for questions."""
    model = Question
    extra = 0
    fields = ['text', 'image', 'order', 'difficulty_level', 'tags', 'is_active']
    ordering = ['order']


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    """Admin configuration for TicketCategory model."""
    
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """Admin configuration for Ticket model."""
    
    list_display = [
        'number', 'title', 'category', 'status', 'questions_count',
        'created_by', 'created_at', 'published_at'
    ]
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['number', 'title', 'description']
    ordering = ['order', 'number']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('number', 'title', 'description', 'category')
        }),
        ('Status', {
            'fields': ('status', 'order')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['questions_count', 'created_at', 'updated_at', 'published_at']
    
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new ticket."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for Question model."""
    
    list_display = [
        'ticket', 'order', 'text_short', 'difficulty_level', 
        'tags', 'is_active', 'created_by', 'created_at'
    ]
    list_filter = ['ticket', 'difficulty_level', 'is_active', 'created_at']
    search_fields = ['text', 'explanation', 'tags']
    ordering = ['ticket', 'order']
    
    fieldsets = (
        ('Question', {
            'fields': ('ticket', 'text', 'image', 'order', 'difficulty_level', 'tags')
        }),
        ('Explanation', {
            'fields': ('explanation', 'explanation_image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [AnswerOptionInline]
    
    def text_short(self, obj):
        """Short version of question text."""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Question Text'
    
    def save_model(self, request, obj, form, change):
        """Set created_by when creating new question."""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    """Admin configuration for AnswerOption model."""
    
    list_display = [
        'question', 'order', 'text_short', 'option_type', 
        'is_correct', 'created_at'
    ]
    list_filter = ['option_type', 'is_correct', 'created_at']
    search_fields = ['text', 'question__text']
    ordering = ['question', 'order']
    
    fieldsets = (
        ('Option', {
            'fields': ('question', 'text', 'image', 'option_type', 'order', 'is_correct')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def text_short(self, obj):
        """Short version of option text."""
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj.text
    text_short.short_description = 'Option Text'


@admin.register(UserTicketProgress)
class UserTicketProgressAdmin(admin.ModelAdmin):
    """Admin configuration for UserTicketProgress model."""
    
    list_display = [
        'user', 'ticket', 'is_completed', 'attempts_count', 
        'best_score', 'correct_answers_count', 'updated_at'
    ]
    list_filter = ['is_completed', 'ticket', 'updated_at']
    search_fields = ['user__display_name', 'ticket__number', 'ticket__title']
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Progress', {
            'fields': ('user', 'ticket', 'is_completed', 'completed_at')
        }),
        ('Statistics', {
            'fields': ('attempts_count', 'best_score', 'total_questions_answered', 'correct_answers_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']

