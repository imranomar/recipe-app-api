"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES # used so that this view would show in swagger


class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Mange the authenticated user"""
    serializer_class =  UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes =  [permissions.IsAuthenticated]

    def get_object(self): # for the htt get request
        """Retrieve and return the authenticated user"""
        return self.request.user #



