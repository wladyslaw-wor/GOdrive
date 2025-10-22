from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileUpdateSerializer, UserStatsSerializer
from .authentication import TelegramAuthentication

User = get_user_model()


class UserProfileView(APIView):
    """User profile management."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        """Update user profile."""
        serializer = UserProfileUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserStatsView(APIView):
    """User statistics."""
    
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user statistics."""
        # Update statistics before returning
        if hasattr(request.user, 'statistics'):
            request.user.statistics.update_statistics()
        
        serializer = UserStatsSerializer(request.user)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_activity(request):
    """Update user's last activity timestamp."""
    request.user.update_activity()
    return Response({'status': 'success'})

