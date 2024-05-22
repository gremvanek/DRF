
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from course.models import Product
from course.services import retrieve_checkout_session, create_checkout_session, create_price, create_product
from users.models import User, Payment
from users.serializers import UserSerializer, UserProfileSerializer


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


class PaymentViewSet(viewsets.ViewSet):
    # Указываем URL-адрес для create_payment
    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        product_name = request.data.get("name")
        product_description = request.data.get("description")
        amount = request.data.get("amount")
        success_url = request.data.get("success_url")
        cancel_url = request.data.get("cancel_url")

        product = create_product(product_name, product_description)
        price = create_price(product['id'], amount)

        checkout_session = create_checkout_session(price['id'], success_url, cancel_url)

        new_product = Product.objects.create(
            name=product_name,
            description=product_description,
            stripe_product_id=product['id']
        )

        new_payment = Payment.objects.create(
            product=new_product,
            amount=amount // 100,
            stripe_price_id=price['id'],
            stripe_checkout_session_id=checkout_session['id'],
            stripe_payment_url=checkout_session['url']
        )

        return Response({
            "payment_url": new_payment.stripe_payment_url
        }, status=status.HTTP_201_CREATED)

    # Указываем URL-адрес для check_payment_status
    @action(detail=True, methods=['get'])
    def check_payment_status(self, pk=None):
        payment = Payment.objects.get(pk=pk)
        session = retrieve_checkout_session(payment.stripe_checkout_session_id)
        return Response(session)
