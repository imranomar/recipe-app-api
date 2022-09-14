"""
Views for the recipe APIS
"""

from rest_framework import viewsets

from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from .serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = RecipeDetailSerializer
    queryset =  Recipe.objects.all() # set the queryset of the ModelView
    authentication_classes = [TokenAuthentication] # set the authentication_classes of the ModelView
    permission_classes = [IsAuthenticated] # set the permission_classes of the ModelView

    #Over-ride queryset method to get the recipes only for the logged in user
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # Over-ride to change serializer_class depending on the action called. default is set above
    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class

    # Over-ride to create a record - need to add user field
    # Serializer should be a validated serializer
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)



class TagViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = TagSerializer
    queryset =  Tag.objects.all() # set the queryset of the ModelView
    authentication_classes = [TokenAuthentication] # set the authentication_classes of the ModelView
    permission_classes = [IsAuthenticated] # set the permission_classes of the ModelView

    #Over-ride queryset method to get the tags only for the logged in user
    def get_queryset(self):
        """Retrieve recipes for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # Over-ride to create a record,  - need to add user fiel, Serializer should be a validated serializer
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)






