from django.urls import path
from rest_framework.routers import SimpleRouter

from course.views import CourseViewSet, LessonListApiView, LessonRetrieveAPIView, LessonCreateApiView, \
    LessonDestroyAPIView, LessonUpdateAPIView
from course.apps import CourseConfig

app_name = CourseConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name='lesson_list'),
    path("lessons/<int:pk>", LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path("lessons/create/", LessonCreateApiView.as_view(), name='lesson_create'),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name='lesson_update'),
]

urlpatterns += router.urls
