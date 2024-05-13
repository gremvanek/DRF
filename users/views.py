from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserProfileSerializer
from rest_framework.filters import OrderingFilter


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_set_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        user.payments = user.payment_set.all()
        return user
