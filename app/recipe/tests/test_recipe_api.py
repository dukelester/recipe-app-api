''' Test for Recipe APIS '''

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def create_recipe(user, **params):
    ''' Create and return a sample recipe '''
    defaults = {
        'title': ' Sample recipe Title',
        'time_in_minutes': 10,
        'price': Decimal('9.89'),
        'description': 'Sample Recipe description here',
        'link': 'https://samplerecipe.com/sample_recipe.pdf'
    } | params
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITests(TestCase):
    ''' Test unauthenticated API Requests '''
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        ''' Test auth is required '''
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    ''' Test authenticated API requests '''
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='recipetest@gmail.com',
            password='recipes10202',
            phone_number='0978230012',
            name='Cheff Natama'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        ''' Get a list of recipes '''
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        ''' Test list the recipes for authenticated user '''
        other_user = get_user_model().objects.create_user(
            email='hamy@gmail.com',
            password='recipes45202',
            phone_number='0908230012',
            name='Harmy Mart'
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
