from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def admin_dashboard(request):
    if request.user.role.role_id != "R1":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(
        request,
        "sports_hub_app/dashboard/admin_dashboard.html"
    )

@login_required
def manager_dashboard(request):
    if request.user.role.role_id != "R2":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(
        request,
        "sports_hub_app/dashboard/manager_dashboard.html"
    )


@login_required
def staff_dashboard(request):
    if request.user.role.role_id != "R3":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(
        request,
        "sports_hub_app/dashboard/staff_dashboard.html"
    )


@login_required
def customer_service_dashboard(request):
    if request.user.role.role_id != "R4":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(
        request,
        "sports_hub_app/dashboard/customer_service_dashboard.html"
    )


@login_required
def customer_dashboard(request):
    if request.user.role.role_id != "R5":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(
        request,
        "sports_hub_app/dashboard/customer_dashboard.html"
    )