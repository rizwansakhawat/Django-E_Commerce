from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )
    newsletter_subscription = models.BooleanField(default=False)
    
    # Preferences
    preferred_currency = models.CharField(max_length=3, default='USD')
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('shipping', 'Shipping Address'),
        ('billing', 'Billing Address'),
        ('both', 'Shipping & Billing'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='shipping')
    
    # Address Details
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Address Fields
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Flags
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name_plural = "Addresses"
    
    def __str__(self):
        return f"{self.get_address_type_display()} - {self.full_name} ({self.city})"
    
    def get_full_address(self):
        address = f"{self.street_address}"
        if self.apartment_address:
            address += f", {self.apartment_address}"
        address += f", {self.city}, {self.state} {self.postal_code}, {self.country}"
        return address


class SavedPaymentMethod(models.Model):
    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_payment_methods')
    
    # Card Details
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    card_holder_name = models.CharField(max_length=100)
    card_last_four = models.CharField(max_length=4)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    
    # Stripe Integration
    stripe_payment_method_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Flags
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name_plural = "Saved Payment Methods"
    
    def __str__(self):
        return f"{self.card_holder_name} - {self.get_card_type_display()} ending in {self.card_last_four}"
    
    def is_expired(self):
        from datetime import datetime
        current_date = datetime.now()
        return (self.expiration_year < current_date.year or 
                (self.expiration_year == current_date.year and self.expiration_month < current_date.month))


class UserActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('order_placed', 'Order Placed'),
        ('payment_made', 'Payment Made'),
        ('profile_updated', 'Profile Updated'),
        ('password_changed', 'Password Changed'),
        ('address_added', 'Address Added'),
        ('address_updated', 'Address Updated'),
        ('card_added', 'Payment Method Added'),
        ('wishlist_updated', 'Wishlist Updated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Reference
    order_id = models.IntegerField(blank=True, null=True)
    payment_id = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "User Activities"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"
