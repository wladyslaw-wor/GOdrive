from django.urls import path
from .views import (
    TicketListView, TicketDetailView, TicketForTestingView,
    UserProgressListView, get_random_ticket, get_question_explanation,
    get_user_stats
)

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('<str:number>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('<str:number>/testing/', TicketForTestingView.as_view(), name='ticket-for-testing'),
    path('progress/', UserProgressListView.as_view(), name='user-progress-list'),
    path('random/', get_random_ticket, name='random-ticket'),
    path('questions/<int:question_id>/explanation/', get_question_explanation, name='question-explanation'),
    path('stats/', get_user_stats, name='user-stats'),
]

