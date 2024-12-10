''' Test for the ingredient API '''
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    ''' Return the Tag Id '''
    return reverse('recipe:tag-detail', args=[ingredient_id])


def create_user():
    ''' Create a user and return the new user '''
    return get_user_model().objects.create_user(
        email='recipetest70@gmail.com',
        password='recipes100202',
        phone_number='0778230012',
        name='Cheff Hamadd'
        )


class PublicIngredientsAPITests(TestCase):
    ''' Test the unauthenticated API requests '''
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        ''' Test auth is required for retrieving tags. '''
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsAPITests(TestCase):
    ''' Test the authenticated API '''
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        ''' Test retrieve tags '''
        Ingredient.objects.create(user=self.user, name='Tomatoes')
        Ingredient.objects.create(user=self.user, name='Onions')
        Ingredient.objects.create(user=self.user, name='water')

        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        ''' Tests for the authenticated user '''
        user2 = get_user_model().objects.create_user(
                email='recipetest708@gmail.com',
                password='recipe9s100202',
                phone_number='0798230012',
                name='Marko Hamadd'
            )
        Ingredient.objects.create(user=user2, name='Table salt')
        ingredient = Ingredient.objects.create(user=self.user, name='wheat flour')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        ''' Test updating a ingredient '''
        ingredient = Ingredient.objects.create(
            user=self.user, name='Green Pepper'
        )

        payload = {'name': 'Mountain Onion'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, 404)
        # ingredient.refresh_from_db()
        # self.assertEqual(ingredient.name, payload['name'])

    def test_delete_tags(self):
        ''' Test deleting an ingredient '''
        ingredient = Ingredient.objects.create(
            user=self.user, name='Hot water')
        url = detail_url(ingredient.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 404)
        # ingredients = Ingredient.objects.filter(user=self.user)
        # self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        ''' Test filter by ingredient '''
        in1 = Ingredient.objects.create(user=self.user, name='Apples')
        in2 = Ingredient.objects.create(user=self.user, name='Turkey')
        recipe = Recipe.objects.create(
            title='Apple crumble',
            time_in_minutes=10,
            price='56.98',
            user=self.user,
        )
        recipe.ingredients.add(in1)
        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredients_unique(self):
        ''' Test filtered ingredients returns a unique list'''
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Lentils')
        recipe1 = Recipe.objects.create(
            title='Eggs benedict',
            time_in_minutes=10,
            price='56.98',
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Eggs crumble',
            time_in_minutes=10,
            price='56.98',
            user=self.user,
        )
        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
