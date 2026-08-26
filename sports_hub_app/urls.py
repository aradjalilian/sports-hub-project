from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate_account"),
    path("login/", views.login, name="login"),
    path("totp/", views.totp, name="totp"),
    path("logout/", views.logout, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("products/", views.product_list, name="products"),
    path("products/<str:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("orders/", views.orders, name="orders"),
    path("returns/", views.returns, name="returns"),
    path("refunds/", views.refunds, name="refunds")
]