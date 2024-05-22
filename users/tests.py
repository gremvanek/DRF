import pytest
import requests_mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from course.models import Product
from users.models import Payment
from django.contrib.auth.models import User  # Добавлен импорт модели User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_product_data():
    return {
        "name": "Test Course",
        "description": "This is a test course.",
        "amount": 5000,
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel",
        "stripe_price_id": "123",
        'stripe_checkout_session_id': "123",
        "stripe_payment_url": "https://example.com/"
    }


@pytest.fixture
def mocker_fixture():
    with requests_mock.Mocker() as mocker:
        yield mocker


@pytest.mark.django_db
def test_create_payment(mocker_fixture, api_client, create_product_data):
    mocker_fixture.post("https://api.stripe.com/v1/products", json={"id": "prod_test"})
    mocker_fixture.post("https://api.stripe.com/v1/prices", json={"id": "price_test"})
    mocker_fixture.post("https://api.stripe.com/v1/checkout/sessions", json={"id": "cs_test",
                                                                             "url": "https://stripe.com/test_checkout"})

    response = api_client.post(reverse('users:payment-create-payment'), data=create_product_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert 'payment_url' in response_data
    assert response_data['payment_url'] == "https://stripe.com/test_checkout"

    product = Product.objects.get(name=create_product_data['name'])
    assert product.description == create_product_data['description']
    assert product.stripe_product_id == "prod_test"

    # Here, we create a payment related to the user
    user = User.objects.first()  # Assuming there's at least one user in the database
    payment = Payment.objects.get(user=user)
    assert payment.payment_sum == create_product_data['amount']
    assert payment.payment_method == "1"  # Checking payment method


@pytest.mark.django_db
def test_check_payment_status(mocker):  # Add mocker as an argument
    # Create a product
    product = Product.objects.create(name="Test Course", description="This is a test course.",
                                     stripe_product_id="prod_test")
    # Create a payment
    payment = Payment.objects.create(product=product, payment_sum=5000, payment_method='1',
                                     stripe_price_id="price_test",
                                     stripe_checkout_session_id="cs_test",
                                     stripe_payment_url="https://stripe.com/test_checkout")

    mocker.get(f"https://api.stripe.com/v1/checkout/sessions/{payment.stripe_checkout_session_id}",
               json={"id": "cs_test", "payment_status": "paid"})

    response = mocker.get(reverse('payment-check-payment-status', kwargs={'pk': payment.pk}))

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['id'] == "cs_test"
    assert response_data['payment_status'] == "paid"
