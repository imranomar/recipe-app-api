from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

import tempfile
import os

from PIL import Image


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag
from core.models import recipe_image_file_path
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create nad return a recipe detail url"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def image_upload_url(recipe_id):
    """Create and return an image upload URL"""
    return reverse("recipe:recipe-upload-image",args=[recipe_id])

def create_recipe(user, **params):
    defaults = {
        'title' : "Sample recipe title",
        'time_minutes': 22,
        'price' : Decimal('5.25'),
        'description': 'Sample Descritption',
        'link':'hp',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

def create_the_user(params):
    return User.objects.create_user(**params)


class PublicRecipeApiTests(TestCase):
    """ Test unauthenticated APi Requests ."""



    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(reverse('recipe:recipe-list'))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated api requests"""

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

    def test_retrive_recipes(self):
        """Test retrieving a list of recipies."""


        create_recipe(self.user)
        create_recipe(self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many = True) # many is true as we want to return a list of items and not one only
        #check http response first
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authenticated user only"""

        other_user = create_the_user({'username':'john2',
                                        'email':'jlennon2@beatles.com',
                                        'password':'glass onion2'})

        create_recipe(self.user)
        create_recipe(other_user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user = self.user)

        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        dict_payload = {
            'title' : 'Sample Recipe',
            'time_minutes': 30,
            'price' : Decimal('5.99'),
        }


        #rest_framework.response.Response
        res = self.client.post(RECIPES_URL, dict_payload) # send payload and get the result

        try:
            self.assertEqual(res.status_code, status.HTTP_201_CREATED) # check http response
        except AssertionError as e:
            print("Test Failure. Response:\n" + str(res.data))

        recipe  = Recipe.objects.get(id = res.data['id']) # find the record from the response
        for k,v in dict_payload.items(): #go through all items in the payload and assert them
            self.assertEqual(getattr(recipe, k ), v) #get aatribute
        self.assertEqual(recipe.user, self.user)


    #for example to test if some fields are becoming
    def test_partial_update(self):
        """Test partial update of a recipe."""
        original_link = "aa"

        recipe = create_recipe(
            user= self.user,
            title = "Sample recipe title",
            link = original_link
        )

        payload = {"title":"New recipe title"}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db() # as Django does not automatically updates the object from the db
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link , original_link)
        self.assertEqual(recipe.user, self.user)

    # for example to test if some fields are becoming
    def test_full_update(self):
        """Test partial update of a recipe."""
        original_link = "aa"

        recipe = create_recipe(
            user=self.user,
            title="Sample recipe title",
            link='bb',
            description = "Sample recipe description",
        )

        dict_payload = {
                    "title": "New recipe title",
                    "link":"xx",
                    "description" : "New recipe description",
                    "time_minutes" : 10,
                    "price" :  Decimal("2.50"),
                   }
        url = detail_url(recipe.id)
        res = self.client.put(url, dict_payload) # update the record

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()  # as Django does not automatically updates the object from the db
        for k, v in dict_payload.items():  # go through all items in the payload and assert them
            self.assertEqual(getattr(recipe, k), v)  # get attribute
        self.assertEqual(recipe.user, self.user)


    def test_change_user_returns_eror(self):
        """Test changing the recipe user results in an error"""
        new_user = create_the_user({'email':"blabla@gmail.com", 'password' :"test1234556", 'username' :"test1234556"})
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}

        url = detail_url(recipe.id)

        self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Testing deleing a recipe successful"""
        recipe = create_recipe(user = self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id = recipe.id).exists())

    def test_recipe_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_the_user({'email':"user@test.com", 'password':"test123", 'username':"test1243"})
        recipe = create_recipe(user = new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id = recipe.id).exists())

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')


    def test_filter_by_tags(self):
        """Test filtering recipies by tags"""
        r1 = create_recipe(user=self.user, title="Malai Kofta")
        r2 = create_recipe(user=self.user, title="Chicken Mughlai")

        tag1 = Tag.objects.create(user=self.user, title="Vegetarian")
        tag2 = Tag.objects.create(user=self.user, title="Pakistani")

        r1.tags.add(tag1)
        r2.tags.add(tag2)

        r3 = create_recipe(user=self.user, title = "Vegetable Korma")

        params = {'tags': f'{tag1.id},{tag2.id}'}

        res = self.client.get(RECIPES_URL, params)

        s1 = RecipeSerializer(r1)
        s2 =  RecipeSerializer(r2)
        s3 = RecipeSerializer(r3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)


    # def test_filter_by_ingredients(self):
    #
    #     """Test filtering recipes by ingredients."""
    #     r1 = create_recipe(user=self.user, title="Malai Kofta")
    #     r2 = create_recipe(user=self.user, title="Chicken Mughlai")
    #
    #     in1 = Ingredient.objects.create(user=self.user, name = 'Cream')
    #     in2 = Ingredient.objects.create(user=self.user, name='Chicken')
    #
    #     r3 = create_recipe(user=self.user, title = "Vegetable Korma")
    #
    #     params = {'ingredients': f'{in1.id},{in2.id}'}
    #
    #     res = self.client.get(RECIPES_URL, params)
    #
    #     s1 = RecipeSerializer(r1)
    #     s2 = RecipeSerializer(r2)
    #     s3 = RecipeSerializer(r3)
    #
    #     self.assertIn(s1.data, res.data)
    #     self.assertIn(s2.data, res.data)
    #     self.assertIn(s3.data, res.data)

class ImageUploadTests(TestCase):
    """ Tests for the image upload API"""

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
        self.recipe = create_recipe(user = self.user)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file: #tmp file block, file delete after with
            img = Image.new('RGB', (10,10)) # creat a dummy image to upload
            img.save(image_file, format='JPEG') # save in tmp space
            image_file.seek(0) # pointer go back to beg of file as to upload we need to be at the beg of file
            payload = {'image': image_file} # createa payload
            res = self.client.post(url, payload, format='multipart') # best practice to upload as multipart

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image"""
        url = image_upload_url(self.recipe.id)

        payload = {'image': "notanimage"}  # create payload

        res = self.client.post(url, payload, format='multipart')  # best practice to upload as multipart

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



