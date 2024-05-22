from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny()]

        else:
            permission_classes = super().get_permissions()

        return permission_classes


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        user.payments = user.payment_set.all()
        return user
