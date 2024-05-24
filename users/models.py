from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from course.models import Course, Lesson

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=12, **NULLABLE, verbose_name='телефон')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='город')
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name='аватарка')
    role = models.CharField(max_length=20, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('pk',)


class Payment(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='оплативший_пользователь',
                             related_name='the_user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', related_name='courses',
                               **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', related_name='lessons',
                               **NULLABLE)
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата_оплаты')
    payment_sum = models.PositiveIntegerField(verbose_name='сумма_оплаты')
    payment_method = models.CharField(choices=[('1', 'Наличные'), ('2', 'Перевод')], verbose_name='способ_оплаты',
                                      max_length=10)

    is_paid = models.BooleanField(default=False, verbose_name='статус оплаты')
    session = models.CharField(max_length=180, verbose_name='сессия для оплаты', **NULLABLE)

    def __str__(self):
        return f"{self.user} - {self.payment_date}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)
