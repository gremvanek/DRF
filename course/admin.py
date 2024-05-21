from django.contrib import admin
from course.models import Course, Lesson


@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('name', 'description', 'preview', 'owner',)


@admin.register(Lesson)
class AdminLesson(admin.ModelAdmin):
    list_display = ('name', 'description', 'preview', 'course', 'owner',)
