import unittest
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase, APIClient
from .models import Course, Lesson, User, Payment


class TestPaymentMethods(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            phone="1234567890",
            city="Test City",
            avatar=None,
            role="member",
        )

        self.course = Course.objects.create(
            name="Test Course",
            preview=None,
            description="Test Course Description",
            owner=self.user,
        )

        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Test Lesson Description",
            preview=None,
            video_url="http://example.com/video",
            link="http://example.com/link",
            course=self.course,
            owner=self.user,
        )

        self.payment = Payment.objects.create(
            user=self.user,
            course=self.course,
            lesson=self.lesson,
            payment_sum=100,
            payment_method="1",
        )

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session(self, mock_session_create, mock_price_create, mock_product_create):
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
        mock_price_create.assert_called_once_with(product="prod_test", unit_amount=100, currency="usd")
        mock_session_create.assert_called_once_with(
            payment_method_types=["card"],
            line_items=[{"price": "price_test", "quantity": 1}],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )


class PaymentListCreateRetrieveAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test@example.com",
            phone="1234567890",
            city="Test City",
            avatar=None,
            role="member",
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Test Course",
            preview=None,
            description="Test Course Description",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
        )

    def test_payment_list_api_view(self):
        url = reverse("payment_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_payment_create_api_view(self):
        url = reverse("payment_create")
        data = {
            "course": self.course.id,
            "lesson": self.lesson.id,
            "payment_method": "usd",
            "payment_sum": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)
        created_payment = Payment.objects.first()
        self.assertEqual(created_payment.course, self.course)

    def test_payment_retrieve_api_view(self):
        payment = Payment.objects.create(
            course=self.course,
            lesson=self.lesson,
            payment_method="usd",
            payment_sum=100,
            user=self.user,
        )
        url = reverse("payment_retrieve", kwargs={"pk": payment.pk})
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
        self.course = Course.objects.create(
            name="Test Course",
            preview=None,
            description="Test Course Description",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
        )

    def test_payment_list_api_view(self):
        url = reverse_lazy("users:payment_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_payment_create_api_view(self):
        url = reverse_lazy("users:payment_create")
        data = {
            "course": self.course.id,
            "lesson": self.lesson.id,
            "payment_method": "usd",
            "payment_sum": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.get()
        self.assertEqual(payment.course.id, self.course.id)
        self.assertEqual(payment.lesson.id, self.lesson.id)

    def test_payment_retrieve_api_view(self):
        payment = Payment.objects.create(
            course=self.course,
            lesson=self.lesson,
            payment_method="usd",
            payment_sum=100,
            user=self.user,
        )
        url = reverse("users:payment_retrieve", kwargs={"pk": payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
