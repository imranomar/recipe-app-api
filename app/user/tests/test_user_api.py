from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import reverse

from django.test import TestCase

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_the_user(params):
    """Create and return a new user"""
    return User.objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a suer is succesful"""
        payload = {
            "email":"test@gample.com",
            "password":"testpass123",
            "first_name": "Test name",
            "username": "test123",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data) # check if password is not sent back any how

    def test_user_with_email_already_exists_error(self):
        """Test creating a suer is succesful"""
        payload = {
            "email": "test@gample.com",
            "password": "testpass123",
            "first_name": "Test name",
            "username": "test123",
        }

        create_the_user(payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars"""

        payload = {
            "email": "test@gample.com",
            "password": "t",
            "first_name": "Test name",
            "username": "test123",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = User.objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """Test generates token for valid credentials"""

        user_details = {
            "email": "test@gample.com",
            "password": "testpass123",
            "first_name": "Test name",
            "username": "test123",
        }

        create_the_user(user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
            "username": user_details['username']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid"""

        data_user = {
            "email": "test@gample.com",
            "password": "goodpass",
            "first_name": "Test name",
            "username": "test123",
        }
        create_the_user(data_user)

        payload = {'email':'test@gmail.com','password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {'email':'test@gmail.com','password':''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retrive_user_unauthorized(self):
        """Test authentication us required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """ Test API requests that require authentication"""

    def setUp(self):
        data_user = {
            "email": "test@gample.com",
            "password": "goodpass",
            "first_name": "Test name",
            "username": "test123",
        }

        self.user = create_the_user(data_user)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data['first_name'],  self.user.first_name)
        self.assertEqual(res.data['email'], self.user.email)


    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the endpoint"""
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""
        payload = {'first_name': "Updated Name", 'password' : "newpassword123"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)