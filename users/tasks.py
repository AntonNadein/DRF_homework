from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import ModelUser


@shared_task
def deactivate_user():
    """Задача блокировки пользователя при бездействии 30 дней"""
    today = timezone.now().date()
    delta_date = today - timedelta(days=30)
    user = ModelUser.objects.filter(is_active=True)
    for u in user:
        if u.last_login:
            if u.last_login.date() < delta_date:
                u.is_active = False
                u.save()
