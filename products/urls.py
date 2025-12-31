from django.urls import path
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('p/', views.product_detail, name='about_us'),
]
