"""
Views for the recipe APIS
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from .serializers import RecipeSerializer, RecipeDetailSerializer, RecipeImageSerializer

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
        elif self.action == 'upload_image': #custom action added to ViewSet besides the ready made list, update, delete
            return RecipeImageSerializer
        return self.serializer_class

    #actions decorator is provided by django framework. action lets you specifily different http methods accepted for the action
    #detail means willl be applied to detail end points meaning an id shouolld be provided.
    #url-path is a custom path for the action
    @action(methods=['Post'], detail=True, url_path="upload-image" )
    def upload_image(self, request, pk= None):
        """Upload an image to recipe."""
        recipe = self.get_object() # get the object of the id passed in the url
        serializer = self.get_object()
        serializer = self.get_serializer(recipe, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    # Over-ride to create a record - need to add user field
    # Serializer should be a validated serializer
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)









