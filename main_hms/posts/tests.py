from django.test import TestCase
from django.urls import reverse

class PostTests(TestCase):
    fixtures = ["posts_posts.json"]

    def test_posts(self):
        url = reverse("posts:posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_create_view(self):
        url = reverse("posts:post_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view(self):
        url = reverse("posts:post_detail", kwargs={"slug": "post2_from_my_email"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_post_update_view(self):
        url = reverse("posts:post_update", kwargs={"slug": "post2_from_my_email"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        url = reverse("posts:post_delete", kwargs={"slug": "post2_from_my_email"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
