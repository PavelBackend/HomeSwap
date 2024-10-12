from django.test import TestCase
from django.urls import reverse
from .models import *

class UserViewTest(TestCase):
    def test_user_detail_view(self):
        url = reverse('users:user_detail', kwargs={'slug': 'test-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_detail.html')
