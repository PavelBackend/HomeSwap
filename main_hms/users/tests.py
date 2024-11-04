from django.test import TestCase
from django.urls import reverse

class UserDetailTestCase(TestCase):
    def setUp(self):
        pass

    # def test_get_user_slug(self):
    #     response = self.client.get(reverse("users:get_user_slug"))
    #     self.assertEqual(response.status_code, 200)

    # def test_user_detail(self):
    #     response = self.client.get(reverse("users:user_detail", kwargs={"slug": self.user.slug}))
    #     self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass
