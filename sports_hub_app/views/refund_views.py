from django.shortcuts import render

def refunds(request):
    return render(request, "sports_hub_app/refund_list.html")