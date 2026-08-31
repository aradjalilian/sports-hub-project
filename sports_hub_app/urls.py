from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("change-password/", views.change_password, name="change_password"),
    path("profile/", views.profile, name="profile"),
    path("profile/update/", views.update_account, name="update_account"),
    path("settings/", views.settings, name="settings"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/manager/", views.manager_dashboard, name="manager_dashboard"),
    path("dashboard/staff/", views.staff_dashboard, name="staff_dashboard"),
    path("dashboard/customer-service/", views.customer_service_dashboard, name="customer_service_dashboard"),
    path("dashboard/customer/", views.customer_dashboard, name="customer_dashboard"),

    path("products/", views.product_list, name="product_list"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/search/", views.product_search, name="product_search"),
    path("products/<str:pk>/", views.product_detail, name="product_detail"),
    path("products/<str:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<str:pk>/delete/", views.product_delete, name="product_delete"),

    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<str:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),

    path("orders/", views.orders, name="orders"),
    path("returns/", views.returns, name="returns"),
    path("refunds/", views.refunds, name="refunds"),
]