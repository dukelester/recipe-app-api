''' Testing the Django admin modifications  '''
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AminSiteTests(TestCase):
    """ Test for the django admin """

    def setUp(self):
        ''' Create user and cleint '''
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com', phone_number='07866373',
            password='admin1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testuser@gmail.com',
            password='testpassword',
            phone_number='079077832',
            name='john mbadi'
        )

    def test_user_list(self):
        ''' Test that the users are listed on the admin '''
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.phone_number)
        self.assertContains(res, self.user.name)
