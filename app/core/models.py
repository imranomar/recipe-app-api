import uuid
import os
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
# Create your models here.
from django.contrib.auth.models import User



class Tag(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=255,validators=[MinLengthValidator(3)] , unique=True )
    created_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

def recipe_image_file_path(instance, filename):
    """Generate file path for new reipe image"""
    ext = os.path.splitext(filename)[1] # get the extension
    filename = f'{uuid.uuid4()}{ext}'
    return os.path.join('uploads','recipe',filename) # join better to create the righ format for os



class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, upload_to = recipe_image_file_path)
    tags = models.ManyToManyField(Tag,null=True, blank=True)

    def __str__(self):
        return self.title
