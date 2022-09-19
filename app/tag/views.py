from django.shortcuts import render

from tag.serializers import TagSerializer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, viewsets
from core.models import Tag
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()  # set the queryset of the ModelView
    authentication_classes = [TokenAuthentication] # set the authentication_classes of the ModelView
    permission_classes = [IsAuthenticated] # set the permission_classes of the ModelView

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id').distinct()  # to only get unique recipies

    # #needed for swagger
    # def get_serializer_class(self):
    #     return self.serializer_class

# class TagAPIView(GenericAPIView):
#     class Meta:
#         model = Tag
#         serializer_class = TagSerializer
#          queryset = Tag.objects.all()
#
#
#
#     def get(self, request):
#         pass
#
#     def post(self, request):
#         """Endpoint to create a new TAG"""
#         serializer = TagSerializer(data=request.data)  # will go to create function of serializer
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#
#     def get_serializer(self):
#         return self.serializer_class
#
# class TagAPIPPDView(GenericAPIView):
#     class Meta:
#         model = Tag
#         serializer_class = TagSerializer
#
#
#
#     def get(self, request):
#         pass
#
#     def patch(self, request):
#         pass
#
#     def put(self, request):
#         pass
#
#     def delete(self, request):
#         pass
#
#     def get_serializer(self):
#         return self.serializer_class