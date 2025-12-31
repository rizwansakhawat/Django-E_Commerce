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
