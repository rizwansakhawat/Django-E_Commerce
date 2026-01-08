from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('product', 'quantity', 'get_unit_price', 'get_subtotal', 'created_at', 'updated_at')
    
    def get_unit_price(self, obj):
        return f"${obj.get_unit_price()}"
    get_unit_price.short_description = 'Unit Price'
    
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'get_total_items', 'get_total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return f"${obj.get_total_price()}"
    get_total_price.short_description = 'Total Price'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'get_unit_price', 'get_subtotal', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_unit_price(self, obj):
        return f"${obj.get_unit_price()}"
    get_unit_price.short_description = 'Unit Price'
    
    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'
