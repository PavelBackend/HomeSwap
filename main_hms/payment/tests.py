from django.test import TestCase
from django.urls import reverse

class PaymentTests(TestCase):
    def test_payment(self):
        url = reverse("payment:checkout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/checkout.html")
    
    def test_complete_order(self):
        url = reverse("payment:complete-order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_payment_failed(self):
        url = reverse("payment:payment-failed")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/payment_failed.html")
    
    def test_payment_success(self):
        url = reverse("payment:payment-success")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payment/payment_success.html")
