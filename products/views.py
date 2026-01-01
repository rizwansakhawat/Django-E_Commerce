from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q, Avg, Count
from .models import Product, Category, Brand, ProductReview

# Create your views here.

class HomeView(TemplateView):
    template_name = 'products/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get promotional products for homepage banner
        context['promotions'] = Product.objects.filter(
            is_promotion=True, 
            is_available=True
        ).select_related('category', 'brand')[:6]
        
        # Get featured/trending products
        context['featured_products'] = Product.objects.filter(
            is_featured=True, 
            is_available=True
        ).select_related('category', 'brand')[:8]
        
        # Get latest products
        context['latest_products'] = Product.objects.filter(
            is_available=True
        ).select_related('category', 'brand').order_by('-created_at')[:8]
        
        # Get categories with product count
        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)
        
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/product.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True).select_related(
            'category', 'brand'
        )
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by brand
        brand_slug = self.kwargs.get('brand_slug')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)
        
        # Price range filter
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        valid_sorts = {
            'popular': '-id',  # Can be changed to view count
            'new': '-created_at',
            'price_low': 'price',
            'price_high': '-price',
            'discount': '-discount_price'
        }
        queryset = queryset.order_by(valid_sorts.get(sort, '-created_at'))
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get category for display
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category'] = get_object_or_404(Category, slug=category_slug)
        
        # Get all categories for sidebar
        context['categories'] = Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)
        
        # Get all brands for filter
        context['brands'] = Brand.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_available=True).select_related(
            'category', 'brand'
        ).prefetch_related(
            'images', 'specifications', 'descriptions', 
            'additional_info', 'reviews__user'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # Get related products from same category
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product.id).select_related('category', 'brand')[:6]
        
        # Get approved reviews
        context['reviews'] = product.reviews.filter(is_approved=True)
        
        # Calculate average rating
        avg_rating = product.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )
        context['avg_rating'] = avg_rating['avg_rating'] or 0
        context['reviews_count'] = product.reviews.filter(is_approved=True).count()
        
        return context


class SearchView(ListView):
    model = Product
    template_name = 'products/search_results.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if query:
            queryset = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(short_description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(sku__icontains=query)
            ).filter(is_available=True).select_related(
                'category', 'brand'
            ).distinct()
        else:
            queryset = Product.objects.none()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_results'] = self.get_queryset().count()
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)


class BrandListView(ListView):
    model = Brand
    template_name = 'products/brands.html'
    context_object_name = 'brands'
    
    def get_queryset(self):
        return Brand.objects.annotate(
            product_count=Count('products')
        ).filter(product_count__gt=0)


def product_detail(request):
    return render(request, 'products/product.html')