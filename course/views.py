from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response

from course.models import Course, Lesson, Product, Payment
from course.paginators import LessonPagination, LearningPagination
from course.permissions import IsModerator, IsOwner
from .models import Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .services import create_product, create_price, create_checkout_session, retrieve_checkout_session


class CourseFilter(filters.FilterSet):
    lesson = filters.CharFilter(field_name="lesson__name", lookup_expr='icontains')

    class Meta:
        model = Course
        fields = ['name', 'lesson']


class LessonFilter(filters.FilterSet):
    class Meta:
        model = Lesson
        fields = ['name']


class IsNotModerator(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_moderator


@method_decorator(name='list', decorator=swagger_auto_schema(operation_description='Показ списка курсов'))
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        else:
            permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]
    pagination_class = LessonPagination
    # filterset_class = LessonFilter


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & (IsModerator | IsOwner)]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated & IsOwner]
    serializer_class = LessonSerializer


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subscription_item = Subscription.objects.filter(user=user, course=course_item).first()

        if subscription_item:
            subscription_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        return Response({'message': message})


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    pagination_class = LearningPagination
    permission_classes = [IsAuthenticated & IsOwner]


class PaymentViewSet(viewsets.ViewSet):
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

    @action(detail=True, methods=['get'])
    def check_payment_status(self, pk=None):
        payment = Payment.objects.get(pk=pk)
        session = retrieve_checkout_session(payment.stripe_checkout_session_id)
        return Response(session)
