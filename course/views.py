from course.models import Course, Lesson
from course.permissions import IsModerator, IsOwner
from course.serializers import LessonSerializer, CourseSerializer

from rest_framework import viewsets, generics


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            # permission_classes = [IsAuthenticated]
            permission_classes = [~IsModerator]

        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsModerator | IsOwner]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsModerator | IsOwner]

        elif self.action in ['destroy']:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]
