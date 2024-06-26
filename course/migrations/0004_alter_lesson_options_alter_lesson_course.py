# Generated by Django 5.0.4 on 2024-06-13 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0003_merge_20240613_1821"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lesson",
            options={},
        ),
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="course.course",
                verbose_name="lessons",
            ),
        ),
    ]
