from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveFromCartView, UpdateCartQuantityView

app_name = 'cart'

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add'),
    path('', CartDetailView.as_view(), name='detail'),
    path('remove/', RemoveFromCartView.as_view(), name='remove'),
    path('update-quantity/', UpdateCartQuantityView.as_view(), name='update_quantity'),
]
