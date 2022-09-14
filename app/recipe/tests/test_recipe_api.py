from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL = reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create nad return a recipe detail url"""
    return reverse("recipe:recipe-detail", args=[recipe_id])

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
        res = self.client.post(RECIPES_URL, dict_payload) # send payload and get the result

        self.assertEqual(res.status_code, status.HTTP_201_CREATED) # check http response
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