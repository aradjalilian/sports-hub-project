from decimal import Decimal
from django.test import TestCase
from sports_hub_app.models import Role, User, Category, Product, CartItem

class UserRegistrationUseCaseTest(TestCase):

    def setUp(self):
        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

    def test_customer_can_be_created_with_customer_role(self):
        user = User.objects.create_user(
            name="New Customer",
            email="newcustomer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=False
        )

        self.assertEqual(
            user.name,
            "New Customer"
        )
        self.assertEqual(
            user.email,
            "newcustomer@example.com"
        )
        self.assertEqual(
            user.role.role_id,
            "R5"
        )
        self.assertFalse(
            user.is_active
        )


class ProductBrowsingUseCaseTest(TestCase):

    def setUp(self):
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

    def test_customer_can_browse_products(self):
        response = self.client.get(
            "/products/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Football"
        )

    def test_customer_can_browse_category(self):
        response = self.client.get(
            "/products/?category=Football"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        products = response.context["products"]

        self.assertEqual(
            products.count(),
            1
        )

        self.assertEqual(
            products.first(),
            self.product
        )

    def test_customer_can_search_product(self):
        response = self.client.get(
            "/products/search/?q=Football"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertContains(
            response,
            "Football"
        )


class ShoppingCartUseCaseTest(TestCase):

    def setUp(self):
        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

        self.user = User.objects.create_user(
            name="Customer",
            email="customer@example.com",
            password="TestPassword123",
            role=self.customer_role,
            is_active=True
        )

        self.category = Category.objects.create(
            category_id="C1",
            name="Football"
        )

        self.product = Product.objects.create(
            product_id="P1",
            category=self.category,
            name="Football",
            description="Official football",
            price=Decimal("20.00"),
            stock=100,
            status="Available"
        )

        self.client.force_login(
            self.user
        )

    def test_customer_can_add_product_to_cart(self):
        response = self.client.post(
            "/cart/add/P1/"
        )

        self.assertRedirects(
            response,
            "/cart/"
        )

        self.assertTrue(
            CartItem.objects.filter(
                user=self.user,
                product=self.product
            ).exists()
        )

    def test_customer_can_increase_product_quantity(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        self.client.get(
            f"/cart/increase/{cart_item.id}/"
        )

        cart_item.refresh_from_db()

        self.assertEqual(
            cart_item.quantity,
            2
        )

    def test_customer_can_remove_product_from_cart(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        self.client.get(
            f"/cart/remove/{cart_item.id}/"
        )

        self.assertFalse(
            CartItem.objects.filter(
                id=cart_item.id
            ).exists()
        )


class RoleBasedAccessUseCaseTest(TestCase):

    def setUp(self):
        self.admin_role = Role.objects.create(
            role_id="R1",
            role_name="Admin"
        )

        self.manager_role = Role.objects.create(
            role_id="R2",
            role_name="Manager"
        )

        self.staff_role = Role.objects.create(
            role_id="R3",
            role_name="Staff"
        )

        self.customer_service_role = Role.objects.create(
            role_id="R4",
            role_name="Customer Service"
        )

        self.customer_role = Role.objects.create(
            role_id="R5",
            role_name="Customer"
        )

    def create_user(self, email, role):
        return User.objects.create_user(
            name="Test User",
            email=email,
            password="TestPassword123",
            role=role,
            is_active=True
        )

    def test_admin_can_access_admin_dashboard(self):
        user = self.create_user(
            "admin@example.com",
            self.admin_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/admin/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_manager_can_access_manager_dashboard(self):
        user = self.create_user(
            "manager@example.com",
            self.manager_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/manager/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_staff_can_access_staff_dashboard(self):
        user = self.create_user(
            "staff@example.com",
            self.staff_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/staff/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_customer_service_can_access_customer_service_dashboard(self):
        user = self.create_user(
            "service@example.com",
            self.customer_service_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/customer-service/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_customer_can_access_customer_dashboard(self):
        user = self.create_user(
            "customer@example.com",
            self.customer_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/customer/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_customer_cannot_access_staff_dashboard(self):
        user = self.create_user(
            "customer2@example.com",
            self.customer_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/staff/"
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_staff_cannot_access_manager_dashboard(self):
        user = self.create_user(
            "staff2@example.com",
            self.staff_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/manager/"
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_customer_service_cannot_access_admin_dashboard(self):
        user = self.create_user(
            "service2@example.com",
            self.customer_service_role
        )

        self.client.force_login(user)

        response = self.client.get(
            "/dashboard/admin/"
        )

        self.assertEqual(
            response.status_code,
            403
        )