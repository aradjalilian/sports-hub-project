from django.shortcuts import render, get_object_or_404
from sports_hub_app.models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, "sports_hub_app/product_list.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, "sports_hub_app/product_detail.html", {"product": product})
