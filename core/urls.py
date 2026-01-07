from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('contact/', views.ContactUsView.as_view(), name='contact'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('policy/', views.PolicyView.as_view(), name='policy'),
]
