from django.contrib import admin
from django.db import models
from .models import Recipe


# Register your models here.
admin.site.register(Recipe)