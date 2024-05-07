from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from course.models import Lesson, Course
from course.serializers import LessonSerializer, CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = LessonSerializer


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseSerializer


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseSerializer


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseSerializer


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CourseSerializer
