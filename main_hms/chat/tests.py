from django.test import TestCase
from django.urls import reverse

class ChatTests(TestCase):
    fixtures = ["users_user.json"]

    def setUp(self):
        self.client.login(username="user_20", password="user_20")

    def test_index_chat(self):
        path = reverse("chat:chat_room", kwargs={"room_name": "test_room"})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/chat.html")
