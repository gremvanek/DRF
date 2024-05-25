import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate, APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.test import TestCase
from users.models import Payment
from users.views import PaymentCreateAPIView


# class TestPaymentMethods(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             email="test@example.com",
#             phone="1234567890",
#             city="Test City",
#             avatar=None,
#             role="member",
#         )
#
#         self.course = Course.objects.create(
#             name="Test Course",
#             preview=None,
#             description="Test Course Description",
#             owner=self.user,
#         )
#
#         self.lesson = Lesson.objects.create(
#             name="Test Lesson",
#             description="Test Lesson Description",
#             preview=None,
#             video_url="http://example.com/video",
#             link="http://example.com/link",
#             course=self.course,
#             owner=self.user,
#         )
#
#         self.payment = Payment.objects.create(
#             user=self.user,
#             course=self.course,
#             lesson=self.lesson,
#             payment_sum=100,
#             payment_method="1",
#         )
#
#     @patch("stripe.Product.create")
#     @patch("stripe.Price.create")
#     @patch("stripe.checkout.Session.create")
# def test_create_checkout_session(self, mock_session_create, mock_price_create, mock_product_create):
#     mock_product_create.return_value.id = "prod_test"
#     mock_price_create.return_value.id = "price_test"
#     mock_session_create.return_value.id = "session_test"
#     mock_session_create.return_value.url = "http://example.com/session"
#
#     success_url = "http://example.com/success"
#     cancel_url = "http://example.com/cancel"
#
#     # Метод create_checkout_session должен быть частью модели Payment
#     session_id, session_url = self.payment.create_checkout_session(
#         product_name="Test Product",
#         price=10000,
#         success_url=success_url,
#         cancel_url=cancel_url,
#     )
#
#     self.assertEqual(session_id, "session_test")
#     self.assertEqual(session_url, "http://example.com/session")
#     self.payment.refresh_from_db()
#     self.assertEqual(self.payment.session_id, "session_test")
#     mock_product_create.assert_called_once_with(name="Test Product", type="service")
#     mock_price_create.assert_called_once_with(product="prod_test", unit_amount=100 * 100, currency="usd")
#     mock_session_create.assert_called_once_with(
#         payment_method_types=["card"],
#         line_items=[{"price": "price_test", "quantity": 1}],
#         mode="payment",
#         success_url=success_url,
#         cancel_url=cancel_url,
#     )


# class PaymentListCreateRetrieveAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create(
#             email="test@example.com",
#             phone="1234567890",
#             city="Test City",
#             avatar=None,
#             role="member",
#         )
#         self.client.force_authenticate(user=self.user)
#         self.course = Course.objects.create(
#             name="Test Course",
#             preview=None,
#             description="Test Course Description",
#             owner=self.user,
#         )
#         self.lesson = Lesson.objects.create(
#             name='Test Lesson',
#             course=self.course,
#         )
#
#     def test_payment_list_api_view(self):
#         url = reverse("payment_list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_payment_create_api_view(self):
#         url = reverse("payment_create")
#         data = {
#             "course": self.course.id,
#             "lesson": self.lesson.id,
#             "payment_method": "usd",
#             "payment_sum": 100,
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Payment.objects.count(), 1)
#         created_payment = Payment.objects.first()
#         self.assertEqual(created_payment.course, self.course)
#
#     def test_payment_retrieve_api_view(self):
#         payment = Payment.objects.create(
#             course=self.course,
#             lesson=self.lesson,
#             payment_method="usd",
#             payment_sum=100,
#             user=self.user,
#         )
#         url = reverse("payment_retrieve", kwargs={"pk": payment.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#
# class PaymentAPITest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             email="test@example.com",
#             phone="1234567890",
#             city="Test City",
#             avatar=None,
#             role="member",
#         )
#         self.client.force_authenticate(user=self.user)
#         self.course = Course.objects.create(
#             name="Test Course",
#             preview=None,
#             description="Test Course Description",
#             owner=self.user,
#         )
#         self.lesson = Lesson.objects.create(
#             name='Test Lesson',
#             course=self.course,
#         )
#
#     def test_payment_list_api_view(self):
#         url = reverse_lazy("users:payment_list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_payment_create_api_view(self):
#         url = reverse_lazy("users:payment_create")
#         data = {
#             "course": self.course.id,
#             "lesson": self.lesson.id,
#             "payment_method": "usd",
#             "payment_sum": 100,
#         }
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Payment.objects.count(), 1)
#         payment = Payment.objects.get()
#         self.assertEqual(payment.course.id, self.course.id)
#         self.assertEqual(payment.lesson.id, self.lesson.id)
#
#     def test_payment_retrieve_api_view(self):
#         payment = Payment.objects.create(
#             course=self.course,
#             lesson=self.lesson,
#             payment_method="usd",
#             payment_sum=100,
#             user=self.user,
#         )
#         url = reverse("users:payment_retrieve", kwargs={"pk": payment.pk})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
User = get_user_model()


class PaymentCreateAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='test@mail.ru', password='password')
        self.factory = APIRequestFactory()
        self.url = '/payments/create/'

    @patch('users.views.rub_converter')
    @patch('users.views.create_stripe_price')
    @patch('users.views.create_stripe_sessions')
    def test_perform_create(self, mock_create_stripe_sessions, mock_create_stripe_price, mock_rub_converter):
        # Настраиваем mock-объекты
        mock_rub_converter.return_value = (100, None)
        mock_create_stripe_price.return_value = 'stripe_price_id'
        mock_create_stripe_sessions.return_value = ('session_id', 'http://payment_link')

        # Данные для POST-запроса
        data = {
            'payment_sum': 1000,
            'payment_method': '1'  # Добавьте поле payment_method
        }

        # Создание запроса
        request = self.factory.post(self.url, data, format='json')
        force_authenticate(request, user=self.user)
        view = PaymentCreateAPIView.as_view()

        # Выполнение запроса и проверка ответа
        response = view(request)

        # Вывод содержимого ответа для отладки
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка созданного объекта Payment
        payment = Payment.objects.get()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.payment_sum, 1000)
        self.assertEqual(payment.session_id, 'session_id')
        self.assertEqual(payment.link, 'http://payment_link')

        # Проверка вызовов mock-объектов
        mock_rub_converter.assert_called_once_with(1000)
        mock_create_stripe_price.assert_called_once_with(100)
        mock_create_stripe_sessions.assert_called_once_with('stripe_price_id')


if __name__ == "__main__":
    unittest.main()
