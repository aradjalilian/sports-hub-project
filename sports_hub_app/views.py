from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_otp import devices_for_user, login as otp_login
import os
import resend
from .models import Product, User, Role

def home(request):
    return render(
        request,
        "sports_hub_app/home.html"
    )


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "sports_hub_app/product_list.html",
        {
            "products": products
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        product_id=product_id
    )

    return render(
        request,
        "sports_hub_app/product_detail.html",
        {
            "product": product
        }
    )


def cart(request):
    return render(
        request,
        "sports_hub_app/cart.html"
    )


def orders(request):
    return render(
        request,
        "sports_hub_app/dorder_history.html"
    )


def returns(request):
    return render(
        request,
        "sports_hub_app/return_list.html"
    )


def refunds(request):
    return render(
        request,
        "sports_hub_app/refund_list.html"
    )


def register(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not name:
            messages.error(
                request,
                "Name is required."
            )
            return render(
                request,
                "sports_hub_app/accounts/register.html"
            )

        if not email:
            messages.error(
                request,
                "Email is required."
            )
            return render(
                request,
                "sports_hub_app/accounts/register.html"
            )

        if not password:
            messages.error(
                request,
                "Password is required."
            )
            return render(
                request,
                "sports_hub_app/accounts/register.html"
            )

        if password != password_confirm:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(
                request,
                "sports_hub_app/accounts/register.html"
            )

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Account with this email already exists."
            )
            return render(
                request,
                "sports_hub_app/accounts/register.html"
            )

        customer_role = Role.objects.get(
            role_id="R5"
        )

        user = User.objects.create_user(
            name=name,
            email=email,
            password=password,
            role=customer_role,
            is_active=False
        )

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(
            user
        )

        activation_url = request.build_absolute_uri(
            reverse(
                "activate_account",
                kwargs={
                    "uidb64": uid,
                    "token": token
                }
            )
        )

        email_html = render_to_string(
            "sports_hub_app/accounts/activation_email.html",
            {
                "user": user,
                "activation_url": activation_url
            }
        )

        resend.api_key = os.environ.get(
            "RESEND_API_KEY"
        )

        resend.Emails.send({
            "from": os.environ.get(
                "RESEND_FROM_EMAIL"
            ),
            "to": [user.email],
            "subject": "Activate your SportsHub account",
            "html": email_html
        })

        messages.success(
            request,
            "Account created. Please check your email to activate your account."
        )

        return redirect("login")

    return render(
        request,
        "sports_hub_app/accounts/register.html"
    )


def activate_account(request, uidb64, token):
    try:
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(
            pk=uid
        )

    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist
    ):
        user = None

    if (
        user is not None
        and default_token_generator.check_token(
            user,
            token
        )
    ):
        user.is_active = True

        user.save(
            update_fields=["is_active"]
        )

        messages.success(
            request,
            "Your account has been activated. You can now log in."
        )

        return redirect("login")

    messages.error(
        request,
        "The activation link is invalid or has expired."
    )

    return redirect("login")


def login(request):
    if request.method == "POST":
        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None and user.is_active:
            request.session[
                "pre_2fa_user_id"
            ] = user.pk

            return redirect("totp")

        messages.error(
            request,
            "Invalid email or password."
        )

    return render(
        request,
        "sports_hub_app/accounts/login.html"
    )


def logout(request):
    auth_logout(request)

    messages.success(
        request,
        "You are logged out."
    )

    return redirect("home")


def totp(request):
    user_id = request.session.get(
        "pre_2fa_user_id"
    )

    if not user_id:
        return redirect("login")

    try:
        user = User.objects.get(
            pk=user_id
        )

    except User.DoesNotExist:
        request.session.pop(
            "pre_2fa_user_id",
            None
        )

        return redirect("login")

    if request.method == "POST":
        otp = request.POST.get(
            "otp",
            ""
        ).strip()

        for device in devices_for_user(
            user,
            confirmed=True
        ):
            if device.verify_token(otp):
                auth_login(
                    request,
                    user
                )

                otp_login(
                    request,
                    device
                )

                request.session.pop(
                    "pre_2fa_user_id",
                    None
                )

                messages.success(
                    request,
                    "You are logged in."
                )

                return redirect("home")

        messages.error(
            request,
            "Invalid authentication code."
        )

    return render(
        request,
        "sports_hub_app/accounts/totp.html"
    )


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get(
            "email",
            ""
        ).strip()

        if not email:
            messages.error(
                request,
                "Email is required."
            )

            return render(
                request,
                "sports_hub_app/accounts/forgot_password.html"
            )

        messages.success(
            request,
            "If an account exists for this email, password reset instructions will be sent."
        )

        return redirect("login")

    return render(
        request,
        "sports_hub_app/accounts/forgot_password.html"
    )


@login_required
def profile(request):
    return render(
        request,
        "sports_hub_app/users/profile.html"
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Your password is changed."
            )

            return redirect("profile")

    else:
        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "sports_hub_app/accounts/change_password.html",
        {
            "form": form
        }
    )


@login_required
def dashboard(request):
    return render(
        request,
        "sports_hub_app/users/dashboard.html"
    )