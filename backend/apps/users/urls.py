from django.urls import path
from .views import UserProfileView, UserStatsView, update_user_activity

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('activity/', update_user_activity, name='user-activity'),
]

