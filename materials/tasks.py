from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_subscriber_email(email_list):
    send_mail(
        subject="Изменения в курсе.",
        message="У нас произошли изменения на курсе",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=email_list,
    )
