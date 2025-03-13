from django.core.management.base import BaseCommand

from users.models import ModelUser, Payment


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        ModelUser.objects.all().delete()
        Payment.objects.all().delete()
