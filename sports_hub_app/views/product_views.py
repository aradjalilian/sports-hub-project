from django.shortcuts import render, get_object_or_404, redirect
from sports_hub_app.models import Product
from sports_hub_app.forms import ProductForm


def product_list(request):
    products = Product.objects.all()
    return render(
        request,
        "sports_hub_app/products/product_list.html",
        {"products": products}
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(
        request,
        "sports_hub_app/products/product_detail.html",
        {"product": product}
    )

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(
        request,
        "sports_hub_app/products/product_create.html",
        {"form": form}
    )


def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", pk=pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "sports_hub_app/products/product_edit.html",
        {"form": form, "product": product}
    )


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(
        request,
        "sports_hub_app/products/product_delete.html",
        {"product": product}
    )


def product_search(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(name__icontains=query)

    return render(
        request,
        "sports_hub_app/products/product_search.html",
        {"results": results, "query": query}
    )