from django.contrib import admin
from .models import UserProfile, Address, SavedPaymentMethod, UserActivity

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender', 'newsletter_subscription', 'created_at')
    list_filter = ('gender', 'newsletter_subscription', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('avatar', 'phone', 'date_of_birth', 'gender', 'bio')
        }),
        ('Preferences', {
            'fields': ('preferred_currency', 'preferred_language', 'newsletter_subscription')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'address_type', 'city', 'state', 'is_default', 'is_active')
    list_filter = ('address_type', 'is_default', 'is_active', 'country', 'created_at')
    search_fields = ('user__username', 'full_name', 'email', 'city')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User & Type', {
            'fields': ('user', 'address_type')
        }),
        ('Contact Information', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Address Details', {
            'fields': ('street_address', 'apartment_address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(SavedPaymentMethod)
class SavedPaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('card_holder_name', 'user', 'card_type', 'card_last_four', 'is_default', 'is_active')
    list_filter = ('card_type', 'is_default', 'is_active', 'created_at')
    search_fields = ('user__username', 'card_holder_name', 'card_last_four', 'stripe_payment_method_id')
    readonly_fields = ('stripe_payment_method_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Card Information', {
            'fields': ('card_type', 'card_holder_name', 'card_last_four', 'expiration_month', 'expiration_year')
        }),
        ('Stripe Integration', {
            'fields': ('stripe_payment_method_id', 'stripe_customer_id')
        }),
        ('Status', {
            'fields': ('is_default', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'ip_address', 'created_at')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'activity_type', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
