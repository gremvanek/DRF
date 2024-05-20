from django.urls import path
from rest_framework.routers import DefaultRouter

from course.apps import CourseConfig
from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
