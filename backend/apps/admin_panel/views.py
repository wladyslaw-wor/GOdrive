from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.users.authentication import TelegramAuthentication

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """Admin dashboard with statistics."""
    if not request.user.is_admin:
        return Response({'error': 'Access denied'}, status=403)
    
    # Get basic statistics
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_attempts': 0,  # Will be calculated from attempts
        'total_tickets': 0,   # Will be calculated from tickets
    }
    
    return Response(stats)

