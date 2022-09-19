""" Serializers for recipe API """

from rest_framework import serializers

from tag.serializers import TagSerializer
from core.models import  Recipe, Tag

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for recipes """

    class Meta:
        model = Recipe
        fields = ["id","title","time_minutes","price","link","tags"]
        read_only_fields = ["id"]

class RecipeDetailSerializer(RecipeSerializer):
    """ Serializers for recipes """
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description','image','tags']


class RecipeImageSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Recipe
        fields = ['id' , 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required':'True'}}


