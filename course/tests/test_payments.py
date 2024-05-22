import pytest
import requests_mock
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from course.models import Product, Payment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_product_data():
    return {
        "name": "Test Course",
        "description": "This is a test course.",
        "amount": 5000,  # in cents
        "success_url": "https://example.com/success",
        "cancel_url": "https://example.com/cancel"
    }


@pytest.mark.django_db
@requests_mock.Mocker()
def test_create_payment(api_client, create_product_data, mocker):
    # Mock Stripe API responses
    mocker.post("https://api.stripe.com/v1/products", json={"id": "prod_test"})
    mocker.post("https://api.stripe.com/v1/prices", json={"id": "price_test"})
    mocker.post("https://api.stripe.com/v1/checkout/sessions",
                json={"id": "cs_test", "url": "https://stripe.com/test_checkout"})

    response = api_client.post(reverse('payment-create-payment'), data=create_product_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert 'payment_url' in response_data
    assert response_data['payment_url'] == "https://stripe.com/test_checkout"

    # Verify data saved in the database
    product = Product.objects.get(name=create_product_data['name'])
    assert product.description == create_product_data['description']
    assert product.stripe_product_id == "prod_test"

    payment = Payment.objects.get(product=product)
    assert payment.amount == create_product_data['amount'] // 100
    assert payment.stripe_price_id == "price_test"
    assert payment.stripe_checkout_session_id == "cs_test"


@pytest.mark.django_db
@requests_mock.Mocker()
def test_check_payment_status(api_client, mocker):
    product = Product.objects.create(name="Test Course", description="This is a test course.",
                                     stripe_product_id="prod_test")
    payment = Payment.objects.create(product=product, amount=5000, stripe_price_id="price_test",
                                     stripe_checkout_session_id="cs_test",
                                     stripe_payment_url="https://stripe.com/test_checkout")

    mocker.get(f"https://api.stripe.com/v1/checkout/sessions/{payment.stripe_checkout_session_id}",
               json={"id": "cs_test", "payment_status": "paid"})

    response = api_client.get(reverse('payment-check-payment-status', kwargs={'pk': payment.pk}))

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['id'] == "cs_test"
    assert response_data['payment_status'] == "paid"
