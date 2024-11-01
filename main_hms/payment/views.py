from django.shortcuts import render
import stripe
from main_hms import settings
from django.shortcuts import render, redirect
from .models import Order
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payment/checkout.html', context)


@csrf_exempt
def complete_order(request):
    if request.method == "POST":
        payment_method = request.POST.get('stripe-payment')

        try:
            charge = stripe.Charge.create(
                amount=5000,
                currency='usd',
                description="Order Payment",
                source=request.POST.get('stripeToken')
            )

            if charge["status"] == "succeeded":
                order = Order.objects.create(
                    user=request.user,
                    amount_paid=charge["amount"] / 100,
                    status="completed"
                )
                order.save()
                return redirect('payment:payment-success')
            else:
                return redirect('payment:payment-failed')
        except stripe.error.StripeError as e:
            messages.error(request, "Ошибка при обработке платежа.")
            return redirect('payment:payment-failed')
    return redirect('payment:checkout')


def payment_success(request):
    return render(request, 'payment/payment_success.html')


def payment_failed(request):
    return render(request, 'payment/payment_failed.html')
