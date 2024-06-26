from django.urls import path
from rest_framework.routers import DefaultRouter

from course.apps import CourseConfig
from course.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
    SubscriptionListAPIView,
    SubscriptionCreateAPIView,
)

app_name = CourseConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_get"),
    path(
        "lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path(
        "subscription/create/",
        SubscriptionCreateAPIView.as_view(),
        name="subscription_create",
    ),
    path(
        "subscription/", SubscriptionListAPIView.as_view(), name="subscription_list"
    ),  # Обработка GET и POST запросов
    path(
        "subscription/delete/",
        SubscriptionListAPIView.as_view(),
        name="subscription_delete",
    ),  # Обработка DELETE запросов
] + router.urls
