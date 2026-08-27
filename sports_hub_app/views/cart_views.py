from django.shortcuts import render, get_object_or_404, redirect
from sports_hub_app.models import CartItem, Product

def calculate_total(cart_items):
    return sum(item.product.price * item.quantity for item in cart_items)

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = calculate_total(cart_items)
    return render(request, "sports_hub_app/cart/view_cart.html", {
        "cart_items": cart_items,
        "total": total
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1},
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("view_cart")

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect("view_cart")

def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect("view_cart")

def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("view_cart")