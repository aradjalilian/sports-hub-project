from django.shortcuts import render

def cart(request):
    return render(request, "sports_hub_app/cart.html")
