from django.contrib import admin
from .models import Order, OrderItem, OrderTracker, Payment

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('unit_price', 'subtotal')


class OrderTrackerInline(admin.TabularInline):
    model = OrderTracker
    extra = 1
    ordering = ['-created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, OrderTrackerInline]
    list_display = ('order_number', 'get_full_name', 'email', 'total_amount', 'order_status', 'payment_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Billing Address', {
            'fields': ('billing_address', 'billing_city', 'billing_state', 'billing_postal_code', 'billing_country')
        }),
        ('Order Status', {
            'fields': ('order_status', 'payment_status', 'payment_method', 'shipped_at', 'delivered_at')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total_amount')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('unit_price', 'subtotal')


@admin.register(OrderTracker)
class OrderTrackerAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number',)
    readonly_fields = ('created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount', 'stripe_status', 'paid_at', 'created_at')
    list_filter = ('payment_method', 'stripe_status', 'created_at')
    search_fields = ('order__order_number', 'stripe_payment_intent_id', 'transaction_id')
    readonly_fields = ('stripe_payment_intent_id', 'stripe_charge_id', 'created_at', 'updated_at', 'paid_at')
    
    fieldsets = (
        ('Order & Amount', {
            'fields': ('order', 'amount', 'currency')
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'card_brand', 'card_last_four')
        }),
        ('Stripe Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_client_secret', 'stripe_charge_id', 'stripe_status')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'receipt_url', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )
