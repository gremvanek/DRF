from rest_framework import serializers

from course.models import Lesson, Course
from course.validators import TitleValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            TitleValidator(field='name'),
            serializers.UniqueTogetherValidator(fields=['name'], queryset=Lesson.objects.all()),
        ]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            TitleValidator(field='name'),
            serializers.UniqueTogetherValidator(fields=['name'], queryset=Lesson.objects.all()),
        ]
