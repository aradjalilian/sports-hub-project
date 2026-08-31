from decimal import Decimal
from django.test import TestCase
from sports_hub_app.models import (
    Role,
    User,
    Category,
    Product,
    Order,
    OrderItem,
    Return,
    Refund,
    CartItem,
)

class RoleModelTest(TestCase):

    def test_role_creation(self):
        role = Role.objects.create(
            role_id="R1",
            role_name="Admin"
        )

        self.assertEqual(role.role_id, "R1")
        self.assertEqual(role.role_name, "Admin")
        self.assertEqual(str(role), "Admin")


class UserModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

    def test_user_creation(self):
        user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.name, "Test User")
        self.assertTrue(user.check_password("TestPassword123"))
        self.assertTrue(user.is_active)
        self.assertEqual(user.role, self.role)

    def test_user_string(self):
        user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.assertEqual(str(user), "test@example.com")

    def test_user_manager_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name="Test User",
                email="",
                password="TestPassword123",
                role=self.role
            )


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(
            category_id="C1",
            name="Football",
            description="Football equipment and clothing."
        )

        self.assertEqual(category.name, "Football")
        self.assertEqual(
            str(category),
            "Football"
        )


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            category_id="C1",
            name="Football",
            description="Football equipment and clothing."
        )

    def test_product_creation(self):
        product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Official football for training matches",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.assertEqual(product.product_id, "P1")
        self.assertEqual(product.name, "Football")
        self.assertEqual(product.price, Decimal("20.00"))
        self.assertEqual(product.stock, 100)
        self.assertEqual(product.status, "Available")

    def test_product_string(self):
        product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Official football for training matches",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.assertEqual(
            str(product),
            "Football"
        )

    def test_category_product_relationship(self):
        product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Official football for training matches",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.assertEqual(
            self.category.products.count(),
            1
        )
        self.assertEqual(
            self.category.products.first(),
            product
        )


class OrderModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

    def test_order_creation(self):
        order = Order.objects.create(
            order_id="O1",
            user=self.user,
            total_price=Decimal("50.00"),
            status="Pending"
        )

        self.assertEqual(order.order_id, "O1")
        self.assertEqual(order.user, self.user)
        self.assertEqual(
            order.total_price,
            Decimal("50.00")
        )
        self.assertEqual(order.status, "Pending")


class OrderItemModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football"
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Football",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.order = Order.objects.create(
            order_id="O1",
            user=self.user,
            total_price=Decimal("40.00"),
            status="Pending"
        )

    def test_order_item_creation(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal("20.00")
        )

        self.assertEqual(item.order, self.order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(
            item.price,
            Decimal("20.00")
        )

    def test_order_item_string(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal("20.00")
        )

        self.assertEqual(
            str(item),
            "O1 - Football"
        )


class ReturnModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football"
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Football",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.order = Order.objects.create(
            order_id="O1",
            user=self.user,
            total_price=Decimal("20.00"),
            status="Completed"
        )

    def test_return_creation(self):
        return_request = Return.objects.create(
            return_id="R100",
            order=self.order,
            product=self.product,
            reason="Damaged product",
            status="Pending"
        )

        self.assertEqual(
            return_request.return_id,
            "R100"
        )
        self.assertEqual(
            return_request.reason,
            "Damaged product"
        )
        self.assertEqual(
            return_request.status,
            "Pending"
        )

    def test_return_string(self):
        return_request = Return.objects.create(
            return_id="R100",
            order=self.order,
            product=self.product,
            reason="Damaged product",
            status="Pending"
        )

        self.assertEqual(
            str(return_request),
            "R100"
        )


class RefundModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football"
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Football",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.order = Order.objects.create(
            order_id="O1",
            user=self.user,
            total_price=Decimal("20.00"),
            status="Completed"
        )

        self.return_request = Return.objects.create(
            return_id="R100",
            order=self.order,
            product=self.product,
            reason="Damaged product",
            status="Approved"
        )

    def test_refund_creation(self):
        refund = Refund.objects.create(
            refund_id="RF1",
            return_request=self.return_request,
            amount=Decimal("20.00"),
            status="Completed"
        )

        self.assertEqual(
            refund.refund_id,
            "RF1"
        )
        self.assertEqual(
            refund.amount,
            Decimal("20.00")
        )
        self.assertEqual(
            refund.status,
            "Completed"
        )

    def test_refund_string(self):
        refund = Refund.objects.create(
            refund_id="RF1",
            return_request=self.return_request,
            amount=Decimal("20.00"),
            status="Completed"
        )

        self.assertEqual(
            str(refund),
            "RF1"
        )


class CartItemModelTest(TestCase):

    def setUp(self):
        self.role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test User",
            email="test@example.com",
            password="TestPassword123",
            role=self.role
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football"
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Football",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

    def test_cart_item_creation(self):
        item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        self.assertEqual(item.user, self.user)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.quantity, 2)

    def test_cart_item_string(self):
        item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        self.assertEqual(
            str(item),
            "test@example.com - Football (2)"
        )