from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, verbose_name='Название курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(max_length=255, verbose_name='Описание курса', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def filter_by_lesson(self, queryset, name, value):
        return queryset.filter(lessons__name=value)


class Lesson(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, verbose_name='Название урока')
    description = models.TextField(max_length=255, verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='lessons/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='URL видео', **NULLABLE)
    link = models.URLField(verbose_name='Ссылка', **NULLABLE)  # Добавлено поле link
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    description = models.TextField()
    stripe_product_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name
