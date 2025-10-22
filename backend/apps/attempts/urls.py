from django.urls import path
from .views import (
    AttemptListView, AttemptDetailView, create_attempt, submit_answer,
    complete_attempt, get_user_statistics, get_attempt_review
)

urlpatterns = [
    path('', AttemptListView.as_view(), name='attempt-list'),
    path('<int:pk>/', AttemptDetailView.as_view(), name='attempt-detail'),
    path('create/', create_attempt, name='create-attempt'),
    path('<int:attempt_id>/submit-answer/', submit_answer, name='submit-answer'),
    path('<int:attempt_id>/complete/', complete_attempt, name='complete-attempt'),
    path('<int:attempt_id>/review/', get_attempt_review, name='attempt-review'),
    path('statistics/', get_user_statistics, name='user-statistics'),
]

