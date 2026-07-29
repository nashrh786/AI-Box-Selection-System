from django.test import TestCase
from .models import Product, ShippingBox, Order, OrderItem
from .services.box_selector import recommend_box
from .services.box_selector import fits


class BoxRecommendationTest(TestCase):

    def setUp(self):
        # Products
        self.laptop = Product.objects.create(
            name="Laptop",
            length=40,
            width=30,
            height=8,
            weight=2.5,
        )

        self.shoes = Product.objects.create(
            name="Shoes",
            length=30,
            width=20,
            height=10,
            weight=1.2,
        )

        self.mug = Product.objects.create(
            name="Mug",
            length=10,
            width=10,
            height=12,
            weight=0.5,
        )

        # Shipping Boxes
        self.small = ShippingBox.objects.create(
            name="Small",
            inner_length=35,
            inner_width=25,
            inner_height=15,
            max_weight=3,
            cost=2.50,
        )

        self.medium = ShippingBox.objects.create(
            name="Medium",
            inner_length=45,
            inner_width=35,
            inner_height=20,
            max_weight=8,
            cost=4.00,
        )

        self.large = ShippingBox.objects.create(
            name="Large",
            inner_length=60,
            inner_width=40,
            inner_height=40,
            max_weight=20,
            cost=7.00,
        )

    def create_order(self, product, quantity):
        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
        )

        return order

    def test_single_laptop_recommends_medium(self):
        order = self.create_order(self.laptop, 1)

        self.assertEqual(
            recommend_box(order),
            self.medium,
        )

    def test_single_shoes_recommends_small(self):
        order = self.create_order(self.shoes, 1)

        self.assertEqual(
            recommend_box(order),
            self.small,
        )

    def test_single_mug_recommends_small(self):
        order = self.create_order(self.mug, 1)

        self.assertEqual(
            recommend_box(order),
            self.small,
        )

    def test_two_laptops_recommendation_exists(self):
        order = self.create_order(self.laptop, 2)

        self.assertIsNotNone(
            recommend_box(order)
        )

    def test_ten_laptops_no_box(self):
        order = self.create_order(self.laptop, 10)

        self.assertIsNone(
            recommend_box(order)
        )

    def test_empty_order_returns_smallest_box(self):
        order = Order.objects.create()

        self.assertEqual(
            recommend_box(order),
            self.small,
        )

    def test_order_has_recommended_box(self):
        order = self.create_order(self.laptop, 1)

        box = recommend_box(order)

        order.recommended_box = box
        order.save()

        order.refresh_from_db()

        self.assertEqual(
            order.recommended_box,
            self.medium,
        )

class ProductModelTest(TestCase):

    def test_product_volume(self):
        product = Product.objects.create(
            name="Box",
            length=10,
            width=5,
            height=2,
            weight=1,
        )

        self.assertEqual(
            product.volume(),
            100
        )

class ShippingBoxModelTest(TestCase):

    def test_box_volume(self):
        box = ShippingBox.objects.create(
            name="Test",
            inner_length=20,
            inner_width=10,
            inner_height=5,
            max_weight=5,
            cost=1,
        )

        self.assertEqual(
            box.volume(),
            1000
        )

class FitsFunctionTest(TestCase):

    def test_product_fits_box(self):

        product = Product.objects.create(
            name="Phone",
            length=10,
            width=5,
            height=2,
            weight=1,
        )

        box = ShippingBox.objects.create(
            name="Box",
            inner_length=15,
            inner_width=10,
            inner_height=5,
            max_weight=2,
            cost=1,
        )

        self.assertTrue(
            fits(product, box)
        )

    def test_product_does_not_fit(self):

        product = Product.objects.create(
            name="TV",
            length=100,
            width=50,
            height=20,
            weight=5,
        )

        box = ShippingBox.objects.create(
            name="Small",
            inner_length=20,
            inner_width=20,
            inner_height=20,
            max_weight=10,
            cost=1,
        )

        self.assertFalse(
            fits(product, box)
        )