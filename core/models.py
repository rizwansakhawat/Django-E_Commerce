from django.db import models
from django.contrib.auth.models import User

# Search Model - For storing search queries and tracking search history
class Search(models.Model):
    query = models.CharField(max_length=255)  # Search query text
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='searches')  # Null for guest users
    results_count = models.PositiveIntegerField(default=0)  # Number of results found
    filters_applied = models.JSONField(default=dict, blank=True)  # JSON: {"category": "mobile", "price_range": "0-1000"}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # For tracking guest user searches

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Searches"

    def __str__(self):
        return f"Search: '{self.query}' - {self.results_count} results"


# Contact Model - For storing contact form submissions
class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='contacts')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True, help_text="Internal notes for admin")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

