from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from course.models import Lesson, Course, Subscription
from course.validators import TitleValidator, LinkValidator, SubscriptionValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            TitleValidator(field='name'),
            serializers.UniqueTogetherValidator(fields=['name'], queryset=Lesson.objects.all()),
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    count_lessons = serializers.SerializerMethodField()

    @extend_schema_field
    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ['name', 'description', 'lessons', 'count_lessons']

    def validate(self, data):
        # Применение TitleValidator
        TitleValidator(field='name')(data)
        # Применение LinkValidator
        LinkValidator('video_url')(data)
        LinkValidator('link')(data)
        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            SubscriptionValidator(),
        ]
