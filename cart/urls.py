from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.add_to_cart, name='add'),
    path('', views.cart_detail, name='detail'),
    path('remove/', views.remove_from_cart, name='remove'),
]
