from django.test import TestCase
from django.urls import reverse

class UserDetailTestCase(TestCase):
    # fixtures = ["users_user.json", "posts_posts.json", "payment_order.json", "chat_message.json"]
    fixtures = ["users_user.json"]

    def setUp(self):
        pass

    def test_user_detail(self):
        url = reverse("users:user_detail", kwargs={"slug": "user_20"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        pass
