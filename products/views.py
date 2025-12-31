from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Product

# Create your views here.

class HomeView(TemplateView):
    template_name = 'products/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promotions'] = Product.objects.filter(is_promotion=True, is_available=True)[:5]
        context['trending_products'] = Product.objects.filter(is_featured=True, is_available=True)[:6]
        return context





def product_detail(request):
    return render(request, 'products/product.html')