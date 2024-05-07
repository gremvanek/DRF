from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):

    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', **NULLABLE)
    city = models.CharField(max_length=35, verbose_name='Город', **NULLABLE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
