from django.shortcuts import render

def orders(request):
    return render(request, "sports_hub_app/order_list.html")