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
from rest_framework import status
from django.shortcuts import reverse
from tag.serializers import TagSerializer
import json
TAGS_URL = reverse('tag:tag-list')



def create_the_user(params):
    return User.objects.create_user(**params)

def create_tag(user, title):
    return Tag.objects.create(user=user ,  title=title)

def detail_url(tag_id):
    """Create nad return a recipe detail url"""
    return reverse("tag:tag-detail", args=[tag_id])

class PublicTagApiTest(TestCase):
    """TEst unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_authentication_required(self):
        """Test auth is rqeuired for retriving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
class PrivateTagsApiTests(TestCase):


    def setUp(self):
        self.client = APIClient()

        data = {
            "email": "test@gample.com",
            "password": "testpass123",
            "first_name": "Test name",
            "username": "test123",
        }

        self.user = create_the_user(data)
        self.client.force_authenticate(self.user)

    def test_rtrieve_tags(self):
        """Test auth is rqeuired for retriving tags
        Note: need to improve to test every tag shold belong to a recipe
        """

        Tag.objects.create(user=self.user, title = "Vegan" )
        Tag.objects.create(user=self.user, title = "Dessert" )


        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        all_tags = TagSerializer(Tag.objects.all().order_by('-id').distinct(), many =True) #returns list rerializer object
        self.assertEqual(json.dumps(res.data), json.dumps(all_tags.data)) #cannot compare array of ordered dics to one another so convert to json
    def test_tags_limited_to_user(self):

        new_user2 = create_the_user({'email': "user2@test.com", 'password': "test1232", 'username': "test12432"})
        self.client.force_authenticate(new_user2)

        Tag.objects.create(user = self.user, title = "Vegan" )
        Tag.objects.create(user = new_user2, title = "Dessert" )

        res = self.client.get(TAGS_URL) #should get all tags of user from end point
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        all_tags_of_user = TagSerializer(Tag.objects.filter(user =  new_user2).order_by('-id').distinct(), many =True) #get tags of user from db
        #try:
        self.assertEqual(json.dumps(res.data),json.dumps(all_tags_of_user.data))  #cannot compare array or ordered dics to one another so convert to json
        #except AssertionError as e:
        #    print("Test Failure. Response:\n" + str(res.data))





