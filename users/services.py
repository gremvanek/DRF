import os
import stripe
from django.conf import settings
stripe.api_key = os.getenv(settings.STRIPE_SECRET_KEY)
from forex_python.converter import CurrencyRates


def rub_converter(amount):
    """Конвертация пендоской валюты в нормальную"""

    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(rate * amount)


def create_stripe_price(amount):
    """Создание цены в стрипе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Course payment"},
    )


def create_stripe_sessions(price):
    """Создание оплаты в stripes"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

# def get_session(instance):
#     """Возаращаем сессию для оплаты курса или урока по API"""
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     product_name = str(instance.user) + str(instance.date_of_payment)
#     product = stripe.Product.create(name=f'{product_name}')
#
#     your_domain = "http://127.0.0.1:8000"
#
#     price = stripe.Price.create(
#         unit_amount=instance.payment_amount,
#         currency='rub',
#         product=f'{product.id}'
#     )
#
#     session = stripe.checkout.Session.create(
#         # payment_method_types=['card'],
#         line_items=[
#             {
#
#                 'price': f"{price.id}",
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url=your_domain + '/success/',
#         cancel_url=your_domain + '/cancel/',
#         # надеюсь сработает
#         customer_email=f"{instance.user.email}",
#     )
#
#     return session
#
#
# def create_product(name, description):
#     return stripe.Product.create(
#         name=name,
#         description=description,
#     )
#
#
# def create_price(product_id, unit_amount, currency="usd"):
#     return stripe.Price.create(
#         product=product_id,
#         unit_amount=unit_amount,
#         currency=currency,
#     )
#
#
# def retrieve_session(session):
#     """Возвращаем obj сессии по АПИ, id передаем в аргумент функц"""
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#
#     return stripe.checkout.Session.retrieve(
#         session,
#     )


def create_checkout_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )


def retrieve_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)
