from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from drf import settings

NULLABLE = {"blank": True, "null": True}


class UserRoles(models.TextChoices):
    MEMBER = "member", _("member")
    MODERATOR = "moderator", _("moderator")


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=12, **NULLABLE, verbose_name="телефон")
    city = models.CharField(max_length=100, **NULLABLE, verbose_name="город")
    avatar = models.ImageField(upload_to="users/", **NULLABLE, verbose_name="аватарка")
    is_moderator = models.BooleanField(verbose_name="Модератор", **NULLABLE)
    role = models.CharField(
        max_length=20,
        choices=UserRoles.choices,
        default=UserRoles.MEMBER,
        verbose_name="роль",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("pk",)


class Payment(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="оплативший_пользователь",
        related_name="the_user",
        **NULLABLE,
    )
    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        verbose_name="оплаченный курс",
        related_name="courses",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        "course.Lesson",
        on_delete=models.CASCADE,
        verbose_name="оплаченный урок",
        related_name="lessons",
        **NULLABLE,
    )
    payment_date = models.DateField(auto_now_add=True, verbose_name="дата_оплаты")
    payment_sum = models.PositiveIntegerField(verbose_name="сумма_оплаты")
    payment_method = models.CharField(
        choices=[("1", "Наличные"), ("2", "Перевод")],
        verbose_name="способ_оплаты",
        max_length=10,
    )
    is_paid = models.BooleanField(default=False, verbose_name="статус оплаты")
    session_id = models.CharField(
        max_length=180,
        verbose_name="сессия для оплаты",
        **NULLABLE,
        help_text="Укажите id сессии",
    )
    link = models.URLField(
        max_length=400,
        **NULLABLE,
        verbose_name="Ссылка для оплаты",
        help_text="Укажите ссылку для оплаты",
    )

    def __str__(self):
        return f"{self.user} - {self.payment_date}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ("-payment_date",)

    # def create_checkout_session(self, product_name, price, success_url, cancel_url):
    #     """Создание сессии оплаты в Stripe"""
    #     try:
    #         converted_price, error = rub_converter(price)
    #         if error:
    #             # Если конвертация не удалась, используем исходную цену
    #             converted_price = price
    #         else:
    #             # Конвертируем цену в копейки для Stripe
    #             converted_price = converted_price * 100
    #
    #         product = stripe.Product.create(name=product_name, type="service")
    #         price = stripe.Price.create(product=product.id, unit_amount=converted_price, currency="usd")
    #         session = stripe.checkout.Session.create(
    #             payment_method_types=["card"],
    #             line_items=[{"price": price.id, "quantity": 1}],
    #             mode="payment",
    #             success_url=success_url,
    #             cancel_url=cancel_url,
    #         )
    #         self.session_id = session.id
    #         self.link = session.url
    #         self.save()
    #         return session.id, session.url
    #     except stripe.error.StripeError as e:
    #         # Обработка ошибок Stripe
    #         return None, str(e)
