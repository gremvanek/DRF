from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_mail_about_updates(course_name=None, recipient_email=None):
    if recipient_email:
        send_mail(
            subject="Уведомление об обновлении курса!",
            message=f"Курс {course_name} обновлен. Ознакомьтесь с новыми материалами!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
