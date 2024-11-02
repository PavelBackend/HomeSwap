from django.shortcuts import render
import stripe
from main_hms import settings
from django.shortcuts import render, redirect
from .models import Order
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    logger.info('Оплата')
    context = {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, 'payment/checkout.html', context)


@csrf_exempt
def complete_order(request):
    logger.info('complete_order')
    if request.method == "POST":
        payment_method = request.POST.get('stripe-payment')

        try:
            logger.info('Попытка оплаты')
            charge = stripe.Charge.create(
                amount=5000,
                currency='usd',
                description="Order Payment",
                source=request.POST.get('stripeToken')
            )

            if charge["status"] == "succeeded":
                logger.info('Оплата прошла успешно')
                order = Order.objects.create(
                    user=request.user,
                    amount_paid=charge["amount"] / 100,
                    status="completed"
                )
                order.save()
                return redirect('payment:payment-success')
            else:
                logger.info('Оплата не прошла')
                return redirect('payment:payment-failed')
        except stripe.error.StripeError as e:
            logger.error(e)
            messages.error(request, "Ошибка при обработке платежа.")
            return redirect('payment:payment-failed')
    return redirect('payment:checkout')


def payment_success(request):
    logger.info('payment_success')
    return render(request, 'payment/payment_success.html')


def payment_failed(request):
    logger.info('payment_failed')
    return render(request, 'payment/payment_failed.html')
