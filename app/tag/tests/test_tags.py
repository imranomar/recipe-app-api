"""
Todo: Test cases
    Deleting Tag
    Creating Tag
    Modifying Tag
    Cannot delete someone else's tag
    Cannot create tag of reciept that does not exist
"""

from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.test import TestCase
from core.models import Tag
from django.shortcuts import reverse

def create_the_user(params):
    return User.objects.create_user(**params)
def create_tag(user, recipe, title):
    return Tag.objects.create(user=user , recipe = recipe, title=title)

def detail_url(tag_id):
    """Create nad return a recipe detail url"""
    return reverse("tag:tag-detail", args=[tag_id])


class PublicTagApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        res = self.client.get('api/tag/tag/')

