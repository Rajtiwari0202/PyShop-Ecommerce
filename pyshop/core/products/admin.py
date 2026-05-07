from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, Category


# ✅ CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


# ✅ PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name']


# (keep others simple for now)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)

from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)