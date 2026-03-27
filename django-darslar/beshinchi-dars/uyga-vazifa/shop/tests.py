from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category, Order, OrderItem, Status, Telefon


class OrderPricingTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="secret123",
        )
        self.category = Category.objects.create(name="Smartfonlar")
        self.telefon = Telefon.objects.create(
            category=self.category,
            name="Galaxy S24",
            brand="Samsung",
            price=Decimal("1200.00"),
            ram=8,
            storage=256,
            battery=5000,
            display_size=Decimal("6.20"),
            main_camera="50MP",
            front_camera="12MP",
            color="Black",
        )

    def test_order_starts_with_zero_total_price(self):
        order = Order.objects.create(user=self.user, status=Status.PENDING)
        self.assertEqual(order.total_price, Decimal("0.00"))

    def test_order_item_copies_phone_price_and_updates_order_total(self):
        order = Order.objects.create(user=self.user, status=Status.PENDING)

        order_item = OrderItem.objects.create(
            order=order,
            telefon=self.telefon,
            quantity=2,
        )

        order.refresh_from_db()
        self.assertEqual(order_item.price, Decimal("1200.00"))
        self.assertEqual(order.total_price, Decimal("2400.00"))

    def test_order_total_recalculates_after_quantity_change_and_delete(self):
        order = Order.objects.create(user=self.user, status=Status.PAID)
        order_item = OrderItem.objects.create(
            order=order,
            telefon=self.telefon,
            quantity=1,
        )

        order_item.quantity = 3
        order_item.save()
        order.refresh_from_db()
        self.assertEqual(order.total_price, Decimal("3600.00"))

        order_item.delete()
        order.refresh_from_db()
        self.assertEqual(order.total_price, Decimal("0.00"))
