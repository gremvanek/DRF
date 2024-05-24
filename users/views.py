from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    PaymentSerializer,
    PaymentRetrieveSerializer,
    PaymentCreateSerializer,
)
from users.services import retrieve_session, get_session


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [AllowAny()]
        else:
            permission_classes = super().get_permissions()
        return permission_classes


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        user = super().get_object()
        user.payments = (
            user.payment_set.all()
        )  # Добавляем связанные платежи к объекту пользователя
        return user


class PaymentListAPIView(generics.ListAPIView):
    """Получаем список Payment"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_type'
    filterset_fields = ("course", "lesson", "payment_method")
    # сортировка по дате оплаты
    ordering_fields = ("date_of_payment",)

    @staticmethod
    def get_success_url():
        return reverse_lazy("payment_list")


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создаем платеж - Payment"""
    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get('lesson')
        course = serializer.validated_data.get('course')
        if not lesson and not course:
            raise ValidationError({
                'non_empty_fields': 'Заполните поле: lesson или course'
            })
        new_pay = serializer.save()
        new_pay.user = self.request.user
        new_pay.session = get_session(new_pay).id
        new_pay.save()

    @staticmethod
    def get_success_url():
        return reverse_lazy("payment_create")


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем список Payment"""

    serializer_class = PaymentRetrieveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        session = retrieve_session(obj.session)
        if session.payment_status == "paid" and session.status == "complete":
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj

    def get_success_url(self):
        return reverse_lazy("payment_retrieve", kwargs={"pk": self.kwargs["pk"]})
