import unittest
from unittest.mock import patch

from django.test import TestCase

from course.models import Lesson, Course
from .models import Payment, User


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


if __name__ == "__main__":
    unittest.main()
