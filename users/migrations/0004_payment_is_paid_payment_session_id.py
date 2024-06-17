# Generated by Django 5.0.4 on 2024-06-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_payment_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="is_paid",
            field=models.BooleanField(default=False, verbose_name="статус оплаты"),
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
