from django.urls import path
from . import views


app_name = "payment"


urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("complete-order/", views.complete_order, name="complete-order"),
    path("payment-success/", views.payment_success, name="payment-success"),
    path("payment-failed/", views.payment_failed, name="payment-failed"),
]

# Тестовая карта
# Номер карты: 4242 4242 4242 4242
# Срок действия: 12/34
# CVC: 123
# Почтовый индекс: 12345
