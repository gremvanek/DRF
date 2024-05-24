from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from users.models import User, Payment
from users.serializers import (
    UserSerializer,
    UserProfileSerializer,
    PaymentSerializer
)
from users.services import rub_converter, create_stripe_price, create_stripe_sessions


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


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_durara = rub_converter(payment.amount)
        price = create_stripe_price(amount_in_durara)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id

# class PaymentListAPIView(generics.ListAPIView):
#     """Получаем список Payment"""
#
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     # Фильтр по 'course', 'lesson', 'payment_type'
#     filter_fields = ("course", "lesson", "payment_method")
#     # сортировка по дате оплаты
#     ordering_fields = ("date_of_payment")
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
#
#
# class PaymentRetrieveAPIView(generics.RetrieveAPIView):
#     """Получаем список Payment"""
#
#     serializer_class = PaymentRetrieveSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Payment.objects.all()
#
#     def get_object(self):
#         obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
#         session = retrieve_session(obj.session)
#         if session.payment_status == "paid" and session.status == "complete":
#             obj.is_paid = True
#             obj.save()
#         self.check_object_permissions(self.request, obj)
#         return obj
