'''
Tests for the user API.
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    ''' Create and return a new user '''
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    ''' Test the public features of the user API '''
    def steUp(self):
        ''' Setup the tests '''
        self.client = APIClient()

    def test_create_user_success(self):
        ''' Create a user successful '''
        payload = {
            'email': 'testuser@gmail.com',
            'phone_number': '0789003044',
            'name': 'Test User',
            'password': 'testpass1234'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_email(self):
        ''' Fails if the email exists '''
        payload = {
            'email': 'testuser@gmail.com',
            'phone_number': '0789003944',
            'name': 'Test User',
            'password': 'testpass5566'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        ''' Create a user with a short password returns an error '''
        payload = {
            'email': 'testuser@gmail.com',
            'phone_number': '0789003944',
            'name': 'Test User',
            'password': 'shw'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_user_with_existing_phone_number(self):
        ''' Fails if the email exists '''
        payload = {
            'email': 'testuser34@gmail.com',
            'phone_number': '0789003944',
            'name': 'Test User',
            'password': 'testpass5566'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
