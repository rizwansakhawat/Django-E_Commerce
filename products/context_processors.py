from django.db.models import Count
from .models import Category, Brand


def navigation_data(request):
    """Provide category and brand data for the global navigation menus."""
    categories = Category.objects.annotate(product_count=Count('products')).filter(product_count__gt=0).order_by('name')
    brands = Brand.objects.annotate(product_count=Count('products')).filter(product_count__gt=0).order_by('-product_count', 'name')[:8]

    return {
        'nav_categories': categories,
        'nav_brands': brands,
    }
