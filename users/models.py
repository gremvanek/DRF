from django.contrib.auth.models import AbstractUser
from django.db import models

from course.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):

    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', **NULLABLE)
    city = models.CharField(max_length=35, verbose_name='Город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='оплативший пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='оплаченный урок', **NULLABLE)
    payment_sum = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(choices=[('1', 'Наличные'), ('2', 'Перевод')], verbose_name='способ оплаты')

    def __str__(self):
        return f"{self.user}: {self.course if self.course else self.lesson} - {self.payment_date}"

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ('-payment_date',)
