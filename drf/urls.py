from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("course.urls", namespace='lesson')),
    path("users/", include("users.urls", namespace='users')),
]
