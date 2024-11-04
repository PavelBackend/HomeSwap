from django.test import TestCase
from django.urls import reverse

class RegAuthTest(TestCase):
    def test_login(self):
        path = reverse("reg_auth:user_login")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        path = reverse("reg_auth:user_registration")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset(self):
        path = reverse("reg_auth:password-reset")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_done(self):
        path = reverse("reg_auth:password-reset-done")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_complete(self):
        path = reverse("reg_auth:password-reset-complete")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        path = reverse("reg_auth:user_logout")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
    
    def test_reg_success(self):
        path = reverse("reg_auth:reg_success")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
    
    def test_auth_success(self):
        path = reverse("reg_auth:auth_success")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
