# Generated by Django 5.0.4 on 2024-05-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_payment_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="session",
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True,
                help_text="Укажите id сессии",
                max_length=180,
                null=True,
                verbose_name="сессия для оплаты",
            ),
        ),
    ]
