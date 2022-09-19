from django.contrib import admin
from django.db import models
from .models import Recipe, Tag


# Register your models here.
admin.site.register(Recipe)
admin.site.register(Tag)