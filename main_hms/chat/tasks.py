from celery import shared_task
from django.core.mail import send_mail
from main_hms import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_notification_to_chat_to_email(email, room_name):
    subject = "Новое сообщение!"
    chat_link = f"{settings.BASE_URL}/chat/{room_name}/"
    message = (
        f"У вас новое сообщение в чате! Перейдите по ссылке для общения: {chat_link}"
    )
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    logger.info("Отправка письма на почту: %s", email)
    send_mail(subject, message, from_email, to_email)
    logger.info("Письмо отправлено на почту: %s", email)
    return "Email sent to recipient"
