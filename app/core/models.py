
from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator
# Create your models here.
from django.contrib.auth.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=255,validators=[MinLengthValidator(3)] , unique=True )
    created_on = models.DateTimeField(auto_now = True)
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.title