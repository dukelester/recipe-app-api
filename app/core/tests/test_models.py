''' Test the models '''
from django.test import TestCase
from django.contrib.auth import get_user_model
import random


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
