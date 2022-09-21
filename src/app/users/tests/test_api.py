from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


REGISTRATION_URL = reverse('rest_register')
LOGIN_URL = reverse('rest_login')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        params = {
            'email': 'test@gmail.com',
            'password1': 'supersecret',
            'password2': 'supersecret'
        }
        res = self.client.post(REGISTRATION_URL, params)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_existing_user(self):
        params1 = {
            'email': 'test@gmail.com',
            'username': 'supersecret',
            'password': 'supersecret'
        }

        params2 = {
            'email': 'test@gmail.com',
            'password1': 'supersecret321',
            'password2': 'supersecret321'
        }
        create_user(**params1)

        res = self.client.post(REGISTRATION_URL, params2)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        params = {
            'email': 'test@gmail.com',
            'password1': 'super',
            'password2': 'super'
        }

        res = self.client.post(REGISTRATION_URL, params)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        params = {
            'email': 'test@gmail.com',
            'username': 'supersecret',
            'password': 'supersecret'
        }
        create_user(**params)

        res = self.client.post(LOGIN_URL, {
            'email': params['email'],
            'password': params['password']
        })

        self.assertIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_invalid_credentials(self):
        params = {
            'email': 'test@gmail.com',
            'username': 'supersecret',
            'password': 'supersecret'
        }
        create_user(**params)

        params2 = {
            'email': 'test@gmail.com',
            'password': 'supersecret1'
        }

        res = self.client.post(LOGIN_URL, params2)
        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_no_user(self):
        """Test that token is not created if user doesn't exists"""
        params = {
            'email': 'test4@gleb.com',
            'password': 'testpass'
        }
        res = self.client.post(LOGIN_URL, params)

        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(LOGIN_URL, {'email': 'abc', 'password': ''})

        self.assertNotIn('key', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)



