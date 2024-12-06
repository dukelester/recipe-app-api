''' Test for Recipe APIS '''

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    ''' Return the url to the recipe '''
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(user, **params):
    ''' Create and return a sample recipe '''
    # Default recipe fields
    defaults = {
        'title': 'Sample recipe Title',
        'time_in_minutes': 10,
        'price': Decimal('9.89'),
        'description': 'Sample Recipe description here',
        'link': 'https://samplerecipe.com/sample_recipe.pdf'
    }
    # Merge defaults with additional parameters
    defaults.update(params)

    # Handle tags if provided
    tags = defaults.pop('tags', [])
    recipe = Recipe.objects.create(user=user, **defaults)

    if tags:
        # Create or get tags and set them on the recipe
        tag_objects = []
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(user=user, **tag_data)
            tag_objects.append(tag)
        recipe.tags.set(tag_objects)  # Assign tags to the recipe

    return recipe


def create_user(**params):
    ''' Create a user and return the new user '''
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(
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
        other_user = create_user(
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

    def test_recipe_detail(self):
        ''' test the recipe details page'''
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)
        serializer = RecipeDetailSerializer(recipe)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_creating_recipe(self):
        ''' Test creating a recipe and storing to the database'''
        payload = {
            'title': 'Sample recipe 2 Title',
            'time_in_minutes': 30,
            'price': Decimal('20.97'),
            'description': 'Sample Recipe 2 description here',
            'link': 'https://samplerecipe.com/sample_recipe2.pdf'
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    def test_partial_recipe_update(self):
        ''' Test the partial update of a recipe '''
        original_link = 'https://samplerecipe.com/sample_recipe3.pdf'
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe 3 Title',
            time_in_minutes=30,
            price=Decimal('20.97'),
            description='Sample Recipe 3 description here',
            link=original_link,
        )
        payload = {'title': 'An amazing egg flat'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        ''' Test full update for the recipe '''
        recipe = create_recipe(
            user=self.user,
            title='Sample recipe 4 Title',
            time_in_minutes=45,
            price=Decimal('120.97'),
            description='Sample Recipe 4 description here',
            link='https://samplerecipe.com/sample_recipe3.pdf',
        )

        payload = {
            'title': 'Sample recipe Updated',
            'time_in_minutes': 30,
            'price': Decimal('320.97'),
            'description': 'Sample Recipe 5 description here',
            'link': 'https://samplerecipe.com/sample_recipe5.pdf'
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(getattr(recipe, key), value)
        self.assertEqual(recipe.user, self.user)

    # def test_create_recipe_with_tags(self):
    #     """Test creating a recipe with tags."""
    #     payload = {
    #         'title': 'Thai Welcome Nuggets',
    #         'time_in_minutes': 45,
    #         'price': '120.97',  # Use a string for Decimal
    #         'description': 'A recipe in Thailand',
    #         'tags': [{'name': 'Thai'}, {'name': 'Dinner'}]  # Nested tag dictionaries
    #     }
    #     res = self.client.post(RECIPE_URL, payload, format='json')  # Specify JSON format
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    #     recipes = Recipe.objects.all()
    #     self.assertEqual(recipes.count(), 1)
    #     recipe = recipes[0]
    #     self.assertEqual(recipe.tags.count(), 2)

    # def test_create_recipe_with_existing_tag(self):
    #     ''' Test creating a recipe with an existing tag '''
    #     tag_indian = Tag.objects.create(user=self.user, name='Indian')
    #     payload = {
    #         'title': 'Sample recipe Updated',
    #         'time_in_minutes': 30,
    #         'price': Decimal('320.97'),
    #         'description': 'Sample Recipe 5 description here',
    #         'tags': [{'name': 'Indian'}, {'name': 'Breakfast'}],
    #     }
    #     res = self.client.post(RECIPE_URL, payload, format='json')

        # self.assertEqual(res.status_code, 400)  # Expect success
        # recipes = Recipe.objects.filter(user=self.user)
        # self.assertEqual(recipes.count(), 1)  # Ensure one recipe is created
        # recipe = recipes[0]
        # self.assertEqual(recipe.tags.count(), 2)

        # Check that the existing tag is associated
        # self.assertIn(tag_indian, recipe.tags.all())

        # # Check that the new tag is created
        # tag_breakfast = Tag.objects.get(user=self.user, name='Breakfast')
        # self.assertIn(tag_breakfast, recipe.tags.all())
