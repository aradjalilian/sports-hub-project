from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from sports_hub_app.forms import ProfileForm


@login_required
def profile(request):
    return render(
        request,
        "sports_hub_app/users/profile.html"
    )


@login_required
def update_account(request):
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Account has been updated."
            )

            return redirect("profile")

    else:
        form = ProfileForm(
            instance=request.user
        )

    return render(
        request,
        "sports_hub_app/users/update_account.html",
        {"form": form}
    )


@login_required
def settings(request):
    return render(
        request,
        "sports_hub_app/users/settings.html"
    )


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user

        auth_logout(request)

        user.delete()

        messages.success(
            request,
            "Your account has been deleted."
        )

        return redirect("home")

    return render(
        request,
        "sports_hub_app/users/delete_account.html"
    )