from django.test import TestCase
from django.urls import reverse


class PostsTestCase(TestCase):
    def test_post_detail_view(self):
        url = reverse("posts:post_detail", kwargs={"slug": "test-slug"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
