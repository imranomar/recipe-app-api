


"""
URL mapping for the recipe app.
"""

from django.urls import (path, include)

from rest_framework.routers import DefaultRouter # a router provided by rest framework , can be used with apiview to automatically create routes for all objects available for that view
from .views import RecipeViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet) # register ViewSet with name recipes. creates end point recipes/ and adds all end points in the viewset

app_name = 'recipe'

urlpatterns = [
    path('',include(router.urls)) # router generates the urls
]