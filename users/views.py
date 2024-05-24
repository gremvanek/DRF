from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from course.validators import LinkValidator
from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    PaymentSerializer,
    PaymentRetrieveSerializer,
    PaymentCreateSerializer,
)


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
        user.payments = user.payment_set.all()
        return user


class PaymentListAPIView(generics.ListAPIView):
    """Получаем список платежей"""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтр по 'course', 'lesson', 'payment_method'
    filterset_fields = ("course", "lesson", "payment_method")
    # сортировка по дате оплаты
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создаем платеж"""

    serializer_class = PaymentCreateSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.validated_data.get("lesson")
        course = serializer.validated_data.get("course")
        if not lesson and not course:
            raise ValidationError(
                {"non_empty_fields": "Заполните поле: lesson или course"}
            )

        # Используем LinkValidator для валидации
        link_validator = LinkValidator(field="your_field_name")
        links_to_validate = [
            serializer.validated_data.get("your_field_name")
        ]  # Замените 'your_field_name' на реальное имя поля

        # Проходимся по ссылкам для валидации
        for link in links_to_validate:
            link_validator(link)

        new_payment = serializer.save(user=self.request.user)
        new_payment.session = new_payment.create_checkout_session(
            product_name="Test Product",  # Название продукта
            price=new_payment.payment_sum,  # Сумма оплаты
            success_url="http://example.com/success",  # URL успешной оплаты
            cancel_url="http://example.com/cancel",  # URL отмены оплаты
        )
        new_payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Получаем платеж"""

    serializer_class = PaymentRetrieveSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        session = obj.retrieve_payment_session()
        if session.payment_status == "paid" and session.status == "complete":
            obj.is_paid = True
            obj.save()
        self.check_object_permissions(self.request, obj)
        return obj
