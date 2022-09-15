"""
URL mapping for the recipe app.
"""

#from django.urls import (path, include)
#from .views import TagViewSet,TagAPIPPDView

# urlpatterns = [
#     path('tags/',TagViewSet.as_view() , name ='list') ,# router generates the urls
#     path('tags/<int:id>',TagAPIPPDView.as_view() , name ='list2') # router generates the urls
# ]

from django.urls import (path, include)
from .views import TagViewSet
from rest_framework.routers import DefaultRouter # a router provided by rest framework , can be used with apiview to automatically create routes for all objects available for that view
from .views import TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet) # register ViewSet with name recipes. creates end point recipes/ and adds all end points in the viewset

app_name = 'tag'

urlpatterns = [
    path('',include(router.urls)) # router generates the urls
]