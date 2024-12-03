''' Test the models '''

import random
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(**params):
    ''' Create a user '''
    return get_user_model().objects.create_user(**params)


class ModelTests(TestCase):
    ''' Test Models '''
    def test_create_user_with_email_successful(self):
        ''' Testing creating a user with an email '''
        email = 'testmail@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            phone_number=f'07239087{random.randrange(2, 100)}',
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        ''' Normalize the user email '''
        sample_emails = [
                        ['test1@EXAMPLE.com', 'test1@example.com'],
                        # ['Test2@example.com', 'test2@example.com'],
                        # ['TEST3@EXAMPLE.COM', 'test3@example.com'],
                        # ['test4@example.com', 'test4@example.com'],
                        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email, 'sample123',
                phone_number=f'07239087{random.randrange(2, 100)}',
                                                        )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """ Test creating a user without email raises an error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '', 'test123',
                phone_number=f'07239087{random.randrange(2, 100)}',)

    def test_new_user_without_phone_raises_error(self):
        ''' Test for a user creation without a phone number '''
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user(
                'hello@example.com', 'hello200',
            )

    def test_new_user_with_empty_phone_raises_error(self):
        ''' Test for a user creation without a phone number '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'hello@example.com', 'hello200', '',
            )

    def test_create_superuser(self):
        ''' Test creating a superuser '''
        user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admin200',
            phone_number=f'07239087{random.randrange(2, 100)}',

        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        ''' Test creating a recipe successfully '''
        user = get_user_model().objects.create_user(
            email='recipeadmin@gmail.com',
            password='recipe101',
            phone_number='0780788990',
            name='John Cheff'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Preparing Carrots with Honey',
            time_in_minutes=5,
            price=Decimal('10.78'),
            description='Sample recipe for my Menu'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        ''' Test Creating a tag is successful '''
        user = create_user(
            email='recipeadmin3@gmail.com',
            password='recipe101',
            phone_number='0780788992',
            name='Mark Cheff'
        )
        tag = models.Tag.objects.create(user=user, name='Tag1')
        self.assertEqual(str(tag), tag.name)
