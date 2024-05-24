import unittest
from unittest.mock import patch
from django.test import TestCase
from rest_framework.reverse import reverse

from .models import User, Payment
from rest_framework.test import APITestCase, APIClient
from .models import Course, Lesson


class TestPaymentMethods(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            phone="1234567890",
            city="Test City",
            avatar=None,
            role="member",
        )

        # Создаем курс
        self.course = Course.objects.create(
            name="Test Course",
            preview=None,
            description="Test Course Description",
            owner=self.user,  # Предполагается, что self.user уже создан
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Lesson Description",
            preview=None,  #
            video_url="http://example.com/video",
            link="http://example.com/link",
            course=self.course,
            owner=self.user,
        )

        # Создаем платеж
        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,  # Используем ранее созданный курс
            lesson=self.lesson,  # Используем ранее созданный урок
            payment_sum=100,
            payment_method="1",
        )

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session(
        self, mock_session_create, mock_price_create, mock_product_create
    ):
        mock_product_create.return_value.id = "prod_test"
        mock_price_create.return_value.id = "price_test"
        mock_session_create.return_value.id = "session_test"

        success_url = "http://example.com/success"
        cancel_url = "http://example.com/cancel"

        session_id = self.payment.create_checkout_session(
            product_name="Test Product",
            price=100,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        self.assertEqual(session_id, "session_test")
        self.assertEqual(self.payment.session, "session_test")
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.session, "session_test")
        mock_product_create.assert_called_once_with(name="Test Product", type="service")
        mock_price_create.assert_called_once_with(
            product="prod_test", unit_amount=100, currency="usd"
        )
        mock_session_create.assert_called_once_with(
            payment_method_types=["card"],
            line_items=[{"price": "price_test", "quantity": 1}],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )


class PaymentListCreateRetrieveAPITest(TestCase):
    def setUp(self):
        # Инициализация клиента API и создание пользователя для аутентификации
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            phone="1234567890",
            city="Test City",
            avatar=None,
            role="member",
        )
        self.client.force_authenticate(user=self.user)
        # Создание объекта Курса для тестирования
        self.course = Course.objects.create(
            name="Test Course",
            preview=None,
            description="Test Course Description",
            owner=self.user,
        )

    def test_payment_list_api_view(self):
        # Тестирование получения списка платежей через API
        url = reverse("payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_payment_create_api_view(self):
        url = reverse("payment-create")
        data = {
            "course": self.course.id,  # Передача ID объекта Курса
            "lesson": "Test Lesson",
            "payment_type": "Test Payment Type",
            "amount": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)
        # Получение созданного объекта Платежа и проверка привязки к Курсу
        created_payment = Payment.objects.first()
        self.assertEqual(created_payment.course, self.course)

    def test_payment_retrieve_api_view(self):
        # Тестирование получения информации о платеже через API
        payment = Payment.objects.create(
            course=self.course,
            lesson="Test Lesson",
            payment_type="Test Payment Type",
            amount=100,
            user=self.user,
        )
        url = reverse("payment-retrieve", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            phone="1234567890",
            city="Test City",
            avatar=None,
            role="member",
        )
        self.client.force_authenticate(user=self.user)

    def test_payment_list_api_view(self):
        url = "/payment/list/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_payment_create_api_view(self):
        url = "/payment/create/"
        data = {
            "course": "Test Course",
            "lesson": "Test Lesson",
            "payment_type": "Test Payment Type",
            "amount": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().course, "Test Course")

    def test_payment_retrieve_api_view(self):
        payment = Payment.objects.create(
            course="Test Course",
            lesson="Test Lesson",
            payment_type="Test Payment Type",
            amount=100,
            user=self.user,
        )
        url = f"/payment/{payment.pk}/retrieve/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
