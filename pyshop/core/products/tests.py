from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Cart, CartItem, Category, Order, Product, Wishlist


class CommerceFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="buyer", password="DemoPass123!")
        self.category = Category.objects.create(name="Workspace")
        self.product = Product.objects.create(
            name="Orbit Keyboard",
            price=Decimal("5999.00"),
            description="Mechanical keyboard for focused work.",
            category=self.category,
        )

    def test_cart_total_uses_decimal_prices(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)

        self.assertEqual(cart.total_price(), Decimal("11998.00"))

    def test_wishlist_is_unique_per_user_and_product(self):
        Wishlist.objects.create(user=self.user, product=self.product)

        with self.assertRaises(Exception):
            Wishlist.objects.create(user=self.user, product=self.product)

    @override_settings(PAYMENT_DEMO_MODE=True)
    def test_demo_checkout_creates_order_and_clears_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=1)
        self.client.login(username="buyer", password="DemoPass123!")

        response = self.client.post(reverse("checkout"))

        self.assertRedirects(response, reverse("order_history"))
        self.assertEqual(Order.objects.filter(user=self.user).count(), 1)
        self.assertFalse(cart.items.exists())
