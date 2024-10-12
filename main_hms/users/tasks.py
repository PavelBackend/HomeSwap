from celery import shared_task
from django.core.mail import send_mail
from main_hms import settings
from .models import Users
from django.core.exceptions import ObjectDoesNotExist


# @shared_task
# def send_test_email():
#     try:
#         user = Users.objects.get(slug=slug)
#     except ObjectDoesNotExist:
#         return f"User {slug} not found"
#     subject = 'Test email'
#     message = 'This is a test email.'
#     from_email = settings.EMAIL_HOST_USER
#     to_email = [user.email]
#     try:
#         send_mail(subject, message, from_email, to_email)
#         return f"Email sent to {user.username}"
#     except Exception as e:
#         return f"Failed to send email to {user.username}: {str(e)}"


@shared_task
def send_test_email():
    subject = 'Test email'
    message = 'This is a test email.'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['pavelsamo555@gmail.com']
    try:
        send_mail(subject, message, from_email, to_email)
        return "Email sent to TestUser"
    except Exception as e:
        return f"Failed to send email to TestUser: {str(e)}"
