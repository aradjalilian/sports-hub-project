from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from sports_hub_app.models import Role, User, Category, Product, CartItem


class RegistrationAndLoginIntegrationTest(TestCase):

    def setUp(self):
        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

    @patch("sports_hub_app.views.account_views.AgentMail")
    def test_registration_creates_inactive_customer(
        self,
        mock_agentmail
    ):
        response = self.client.post(
            "/register/",
            {
                "name": "Test Customer",
                "email": "customer@example.com",
                "password": "TestPassword123",
                "password_confirm": "TestPassword123",
            }
        )

        self.assertRedirects(
            response,
            "/login/"
        )

        user = User.objects.get(
            email="customer@example.com"
        )

        self.assertEqual(
            user.role,
            self.customer_role
        )
        self.assertFalse(user.is_active)

        mock_agentmail.return_value.inboxes.messages.send.assert_called_once()

    def test_login_with_valid_active_user(self):
        user = User.objects.create_user(
            name="Test Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

        response = self.client.post(
            "/login/",
            {
                "email": "customer@example.com",
                "password": "TestPassword123",
            }
        )

        self.assertRedirects(
            response,
            "/"
        )
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            user.pk
        )

    def test_login_with_invalid_password(self):
        User.objects.create_user(
            name="Test Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

        response = self.client.post(
            "/login/",
            {
                "email": "customer@example.com",
                "password": "WrongPassword123",
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "Invalid email or password."
        )

    def test_logout_after_login(self):
        user = User.objects.create_user(
            name="Test Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

        self.client.force_login(user)

        response = self.client.get(
            "/logout/"
        )

        self.assertRedirects(
            response,
            "/login/"
        )

        self.assertNotIn(
            "_auth_user_id",
            self.client.session
        )


class ProductAndCartIntegrationTest(TestCase):

    def setUp(self):
        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Test Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football",
            description="Football equipment and clothing."
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Official football for training matches",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

    def test_add_product_to_cart_and_view_cart(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/cart/add/P1/"
        )

        self.assertRedirects(
            response,
            "/cart/"
        )

        cart_item = CartItem.objects.get(
            user=self.user,
            product=self.product
        )

        self.assertEqual(
            cart_item.quantity,
            1
        )

        response = self.client.get(
            "/cart/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Football"
        )

    def test_add_same_product_twice_increases_quantity(self):
        self.client.force_login(self.user)

        self.client.post(
            "/cart/add/P1/"
        )

        self.client.post(
            "/cart/add/P1/"
        )

        cart_item = CartItem.objects.get(
            user=self.user,
            product=self.product
        )

        self.assertEqual(
            cart_item.quantity,
            2
        )

    def test_increase_cart_quantity(self):
        self.client.force_login(self.user)

        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        response = self.client.get(
            f"/cart/increase/{cart_item.id}/"
        )

        self.assertRedirects(
            response,
            "/cart/"
        )

        cart_item.refresh_from_db()

        self.assertEqual(
            cart_item.quantity,
            2
        )

    def test_decrease_cart_quantity(self):
        self.client.force_login(self.user)

        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        response = self.client.get(
            f"/cart/decrease/{cart_item.id}/"
        )

        self.assertRedirects(
            response,
            "/cart/"
        )

        cart_item.refresh_from_db()

        self.assertEqual(
            cart_item.quantity,
            1
        )

    def test_remove_cart_item(self):
        self.client.force_login(self.user)

        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        response = self.client.get(
            f"/cart/remove/{cart_item.id}/"
        )

        self.assertRedirects(
            response,
            "/cart/"
        )

        self.assertFalse(
            CartItem.objects.filter(
                id=cart_item.id
            ).exists()
        )


class DashboardIntegrationTest(TestCase):

    def setUp(self):
        self.manager_role = Role.objects.create(
            role_id="R2",
            role_name="Manager"
        )

        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.manager = User.objects.create_user(
            name="Manager",
            email="manager@example.com",
            password="TestPassword123",
            role=self.manager_role,
            is_active=True
        )

        self.customer = User.objects.create_user(
            name="Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

    def test_manager_can_access_manager_dashboard(self):
        self.client.force_login(self.manager)

        response = self.client.get(
            "/dashboard/manager/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "sports_hub_app/dashboard/manager_dashboard.html"
        )

    def test_customer_is_forbidden_from_manager_dashboard(self):
        self.client.force_login(self.customer)

        response = self.client.get(
            "/dashboard/manager/"
        )

        self.assertEqual(
            response.status_code,
            403
        )