from django.contrib import admin
from .models import Role, User, Product, Order, OrderItem, Return, Refund

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("role_id", "role_name")
    search_fields = ("role_id", "role_name")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "role", "is_active", "is_staff")
    search_fields = ("email", "role_role_name")
    list_filter = ("role", "is_active", "is_staff")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "price", "stock", "status")
    search_fields = ["product_id", "name"]
    list_filter = ["status"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "order_date", "total_price", "status")
    search_fields = ["order_id", "user__email"]
    list_filter = ["status", "order_date"]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    search_fields = ["order__order_id", "product__name"]

@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ("return_id", "order", "product", "reason", "status")
    search_fields = ["return_id", "order__order_id", "product__name"]
    list_filter = ["status"]

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("refund_id", "return_request", "amount", "refund_date", "status")
    search_fields = ["refund_id", "return_request__return_id"]
    list_filter = ["status", "refund_date"]
