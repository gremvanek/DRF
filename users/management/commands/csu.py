from django.core.management import BaseCommand

from drf import settings
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=settings.ROOT_EMAIL,
            first_name="Admin",
            last_name="SkyPro",
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(settings.ROOT_PASSWORD)
        user.save()
