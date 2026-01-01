from django.urls import path
from . import views 

app_name = 'product'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Product Listing
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='products_by_category'),
    path('brand/<slug:brand_slug>/', views.ProductListView.as_view(), name='products_by_brand'),
    
    # Product Detail
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Categories & Brands
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
]
