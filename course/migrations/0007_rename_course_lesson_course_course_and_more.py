# Generated by Django 5.0.4 on 2024-05-22 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0006_alter_lesson_options_alter_course_owner_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lesson",
            old_name="course",
            new_name="course_course",
        ),
        migrations.RenameField(
            model_name="subscription",
            old_name="course",
            new_name="course_course",
        ),
    ]