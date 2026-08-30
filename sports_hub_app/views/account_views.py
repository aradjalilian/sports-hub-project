from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from agentmail import AgentMail

from sports_hub_app.forms import RegisterForm, LoginForm
from sports_hub_app.models import User, Role


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            default_role = Role.objects.get(role_id="R5")

            user = User.objects.create_user(
                name=name,
                email=email,
                password=password,
                role=default_role,
                is_active=False
            )

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

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
                "sports_hub_app/emails/activation_email.html",
                {
                    "user": user,
                    "activation_url": activation_url
                }
            )

            client = AgentMail(
                api_key=settings.AGENTMAIL_API_KEY
            )

            client.inboxes.messages.send(
                inbox_id=settings.AGENTMAIL_INBOX_ID,
                to=user.email,
                subject="Activate your SportsHub account",
                text=f"Please activate your account: {activation_url}",
                html=email_html
            )

            messages.success(
                request,
                "Account created. Please check your email to activate your account."
            )

            return redirect("login")

        messages.error(
            request,
            "Please correct the errors below."
        )

        return render(
            request,
            "sports_hub_app/accounts/register.html",
            {"form": form}
        )

    form = RegisterForm()

    return render(
        request,
        "sports_hub_app/accounts/register.html",
        {"form": form}
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

    if user and default_token_generator.check_token(
        user,
        token
    ):
        user.is_active = True

        user.save(
            update_fields=["is_active"]
        )

        messages.success(
            request,
            "Your account has been activated."
        )

        return redirect("login")

    messages.error(
        request,
        "Invalid or expired activation link."
    )

    return redirect("login")


def login(request):
    if request.method == "POST":
        form = LoginForm(
            request=request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()

            if user.is_active:
                auth_login(
                    request,
                    user
                )

                return redirect("home")

            messages.error(
                request,
                "Account is not activated."
            )

            return redirect("login")

        messages.error(
            request,
            "Invalid email or password."
        )

        return render(
            request,
            "sports_hub_app/accounts/login.html",
            {"form": form}
        )

    form = LoginForm()

    return render(
        request,
        "sports_hub_app/accounts/login.html",
        {"form": form}
    )


def logout(request):
    auth_logout(request)

    messages.success(
        request,
        "You are logged out."
    )

    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get(
            "email",
            ""
        ).strip()

        messages.success(
            request,
            "If an account exists for this email, reset instructions will be sent."
        )

        return redirect("login")

    return render(
        request,
        "sports_hub_app/accounts/forgot_password.html"
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
                "Your password has been changed."
            )

            return redirect("profile")

    else:
        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "sports_hub_app/accounts/change_password.html",
        {"form": form}
    )