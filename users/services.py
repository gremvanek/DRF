import os
from typing import Tuple

import requests
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def rub_converter(amount: float) -> Tuple[int, None]:

    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        response.raise_for_status()
        data = response.json()
        rate = data["Valute"]["USD"]["Value"]
        return (
            int(rate * amount),
            None,
        )  # Умножаем сумму на курс и преобразуем в целое число
    except requests.exceptions.RequestException as e:
        # Обработка случая, когда сервис недоступен
        print(f"Currency rates are not available: {e}")
        return int(70 * amount), None  # Резервный курс
    except KeyError as e:
        # Обработка случая, когда в ответе нет нужных данных
        print(f"Key error: {e}")
        return int(70 * amount), None  # Резервный курс
    except Exception as e:
        # Другие исключения, которые могут возникнуть при конвертации
        print(f"An error occurred: {e}")
        return int(70 * amount), None  # Резервный курс


def create_stripe_price(amount):
    """Создание цены в стрипе"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Оплата курса"},
    )


def create_stripe_sessions(price):
    """Создание оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def retrieve_session(session):
    """Возвращаем obj сессии по API, id передаем в аргумент функции"""
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    return stripe.checkout.Session.retrieve(session)


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
# def create_checkout_session(price_id, success_url, cancel_url):
#     return stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 "price": price_id,
#                 "quantity": 1,
#             }
#         ],
#         mode="payment",
#         success_url=success_url,
#         cancel_url=cancel_url,
#     )
#
#
# def retrieve_checkout_session(session_id):
#     return stripe.checkout.Session.retrieve(session_id)
