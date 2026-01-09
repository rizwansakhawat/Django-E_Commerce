from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.my_account, name='my_account'),
    
    # Orders
    path('orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('orders/<int:order_id>/', views.UserOrderDetailView.as_view(), name='user_order_detail'),
    
    # Profile Settings
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    
    # Address Management
    path('addresses/', views.AddressListView.as_view(), name='address_list'),
    path('addresses/add/', views.AddressCreateView.as_view(), name='address_add'),
    path('addresses/<int:address_id>/edit/', views.AddressUpdateView.as_view(), name='address_edit'),
    path('addresses/<int:address_id>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
    
    # Activity
    path('activity/', views.UserActivityListView.as_view(), name='user_activity'),
]
