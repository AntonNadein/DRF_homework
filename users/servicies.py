import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создание продукта в страйпе"""
    return stripe.Product.create(name=name)


def create_stripe_price(amount, product):
    """Создание цены в страйпе"""
    return stripe.Price.create(currency="usd", unit_amount=amount * 100, product=product.get("id"))


def create_stripe_session(price):
    """Создание сессии в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
