''' Test the tags API '''
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag, Recipe
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def detail_url(tag_id):
    ''' Return the Tag Id '''
    return reverse('recipe:tag-detail', args=[tag_id])


def create_user(**params):
    ''' Create a user and return the new user '''
    return get_user_model().objects.create_user(**params)


class PublicTagsAPITests(TestCase):
    ''' Test the unauthenticated API requests '''
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        ''' Test auth is required for retrieving tags. '''
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    ''' Test the authenticated API '''
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='recipetest70@gmail.com',
            password='recipes100202',
            phone_number='0778230012',
            name='Cheff Hamadd'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        ''' Test retrieve tags '''
        Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        ''' Tests for the authenticated user '''
        user2 = create_user(
            email='user1@gmail.com',
            password='recipes100202',
            phone_number='0770230012',
            name='Maryland Kimombo')
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        ''' Test updating a tag '''
        tag = Tag.objects.create(
            user=self.user, name='After Dinner'
        )

        payload = {'name': 'After Meals Dissert'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tags(self):
        ''' Test deleting a tag '''
        tag = Tag.objects.create(user=self.user, name='After Breakfast')
        url = detail_url(tag.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())


    def test_filter_tags_assigned_to_recipes(self):
        ''' Test filter by tags '''
        tag1 = Tag.objects.create(user=self.user, name='breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Apple crumble',
            time_in_minutes=10,
            price='56.98',
            user=self.user,
        )
        recipe.tags.add(tag1)
        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(tag1)
        s2 = IngredientSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        ''' Test filtered tags returns a unique list'''
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
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
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)
