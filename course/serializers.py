from rest_framework.serializers import ModelSerializer

from course.models import Lesson, Course


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
