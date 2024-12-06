''' Test the tags API '''


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
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
