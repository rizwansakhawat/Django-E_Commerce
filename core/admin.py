from django.contrib import admin
from .models import Search

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'results_count', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('query',)
    readonly_fields = ('created_at', 'updated_at')
