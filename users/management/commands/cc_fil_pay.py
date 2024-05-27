from datetime import date

from django.core.management.base import BaseCommand

from users.models import Payment, User, Course, Lesson


class Command(BaseCommand):
    help = "Частично оплата по карте, частично наличкой. По четности если четный по карте, если нечетный наличкой"

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            if user.id % 2 == 0:
                payment_method = "card"
                amount = 500
                course = Course.objects.get(id=1)
                lesson = None
            else:
                payment_method = "cash"
                amount = 100
                course = None
                lesson = Lesson.objects.get(id=1)

            Payment.objects.create(
                user=user,
                payment_date=date.today(),
                amount=amount,
                payment_method=payment_method,
                course=course,
                lesson=lesson,
            )
