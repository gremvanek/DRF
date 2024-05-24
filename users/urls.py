from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.apps import UsersConfig
from users.views import (
    UserViewSet,
    UserProfileAPIView,
    PaymentCreateAPIView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"", UserViewSet, basename="users")


urlpatterns = [
    path("user_detail/<int:pk>/", UserProfileAPIView.as_view(), name="user_detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # path('payment/list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    # path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
] + router.urls
