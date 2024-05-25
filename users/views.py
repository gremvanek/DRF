from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    PaymentSerializer, PaymentRetrieveSerializer
)
from users.services import rub_converter, create_stripe_price, create_stripe_sessions, retrieve_session


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        return super().get_permissions()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_rub, error = rub_converter(payment.payment_sum)
        if error:
            raise ValidationError({"payment_sum": error})

        price = create_stripe_price(amount_in_rub)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    """Получаем список Payment"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_method'
    filterset_fields = ("course", "lesson", "payment_method")
    # Сортировка по дате оплаты
    ordering_fields = ["payment_date"]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем детали Payment"""

    serializer_class = PaymentRetrieveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        session = retrieve_session(obj.session_id)
        if session.payment_status == "paid" and session.status == "complete":
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj
#
#
# class PaymentCreateAPIView(generics.CreateAPIView):
#     """ Создаем платеж - Payment"""
#     serializer_class = PaymentCreateSerializer
#     queryset = Payment.objects.all()
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         lesson = serializer.validated_data.get('lesson')
#         course = serializer.validated_data.get('course')
#         if not lesson and not course:
#             raise ValidationError({
#                 'non_empty_fields': 'Заполните поле: lesson или course'
#             })
#         new_pay = serializer.save()
#         new_pay.user = self.request.user
#         new_pay.session = get_session(new_pay).id
#         new_pay.save()

