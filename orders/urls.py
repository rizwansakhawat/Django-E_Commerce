from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/info/', views.checkout_info, name='checkout_info'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
]
