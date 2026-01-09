from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from orders.models import Order, OrderItem
from .models import UserProfile, Address, SavedPaymentMethod, UserActivity
from .forms import UserUpdateForm, ProfileUpdateForm, AddressForm, UserRegistrationForm

# Create your views here.

class UserRegistrationView(CreateView):
    """User registration view"""
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        """Handle successful registration"""
        response = super().form_valid(form)
        
        # Create user profile
        UserProfile.objects.get_or_create(user=self.object)
        
        # Log activity
        UserActivity.objects.create(
            user=self.object,
            activity_type='registration',
            description='User account created'
        )
        
        messages.success(self.request, 'Registration successful! Please log in with your credentials.')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users to home"""
        if request.user.is_authenticated:
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect to next page or dashboard"""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('accounts:my_account')
    
    def form_valid(self, form):
        """Log user activity on login"""
        response = super().form_valid(form)
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='login',
            description='User logged in',
            ip_address=self.get_client_ip()
        )
        return response
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('products:home')
    http_method_names = ['get', 'post', 'options']
    
    def dispatch(self, request, *args, **kwargs):
        """Log user activity on logout"""
        if request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                activity_type='logout',
                description='User logged out'
            )
        return super().dispatch(request, *args, **kwargs)

@login_required(login_url='admin:login')
def my_account(request):
    """User account dashboard"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get addresses
    addresses = Address.objects.filter(user=request.user, is_active=True)[:3]
    
    # Get recent activity
    recent_activity = UserActivity.objects.filter(user=request.user)[:5]
    
    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'addresses': addresses,
        'recent_activity': recent_activity,
    }
    return render(request, 'accounts/my_account.html', context)


class UserOrderListView(LoginRequiredMixin, ListView):
    """Display all orders for the logged-in user"""
    model = Order
    template_name = 'accounts/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    login_url = 'admin:login'
    
    def get_queryset(self):
        """Get orders for the current user"""
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class UserOrderDetailView(LoginRequiredMixin, DetailView):
    """Display details of a specific order"""
    model = Order
    template_name = 'accounts/user_order_detail.html'
    context_object_name = 'order'
    login_url = 'admin:login'
    pk_url_kwarg = 'order_id'
    
    def get_queryset(self):
        """Get only orders belonging to the current user"""
        return Order.objects.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        """Override to check user ownership"""
        if queryset is None:
            queryset = self.get_queryset()
        
        order_id = self.kwargs.get(self.pk_url_kwarg)
        try:
            order = queryset.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404('Order not found')
        
        return order
    
    def get_context_data(self, **kwargs):
        """Add order items to context"""
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context


# Profile Management Views
@login_required(login_url='admin:login')
def profile_settings(request):
    """View and update user profile settings"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='profile_updated',
                description='Profile information updated'
            )
            
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_settings.html', context)


# Address Management Views
class AddressListView(LoginRequiredMixin, ListView):
    """Display all addresses for the logged-in user"""
    model = Address
    template_name = 'accounts/address_list.html'
    context_object_name = 'addresses'
    login_url = 'admin:login'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user, is_active=True)


class AddressCreateView(LoginRequiredMixin, CreateView):
    """Create a new address"""
    model = Address
    form_class = AddressForm
    template_name = 'accounts/address_form.html'
    success_url = reverse_lazy('accounts:address_list')
    login_url = 'admin:login'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # If this is set as default, unset other defaults
        if form.instance.is_default:
            Address.objects.filter(user=self.request.user).update(is_default=False)
        
        # Log activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='address_added',
            description=f'New address added: {form.instance.city}'
        )
        
        messages.success(self.request, 'Address added successfully!')
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing address"""
    model = Address
    form_class = AddressForm
    template_name = 'accounts/address_form.html'
    success_url = reverse_lazy('accounts:address_list')
    login_url = 'admin:login'
    pk_url_kwarg = 'address_id'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        # If this is set as default, unset other defaults
        if form.instance.is_default:
            Address.objects.filter(user=self.request.user).exclude(id=form.instance.id).update(is_default=False)
        
        # Log activity
        UserActivity.objects.create(
            user=self.request.user,
            activity_type='address_updated',
            description=f'Address updated: {form.instance.city}'
        )
        
        messages.success(self.request, 'Address updated successfully!')
        return super().form_valid(form)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    """Soft delete an address"""
    model = Address
    success_url = reverse_lazy('accounts:address_list')
    login_url = 'admin:login'
    pk_url_kwarg = 'address_id'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Soft delete
        self.object.is_active = False
        self.object.save()
        
        messages.success(request, 'Address deleted successfully!')
        return redirect(self.success_url)


# Activity View
class UserActivityListView(LoginRequiredMixin, ListView):
    """Display user activity history"""
    model = UserActivity
    template_name = 'accounts/user_activity.html'
    context_object_name = 'activities'
    paginate_by = 20
    login_url = 'admin:login'
    
    def get_queryset(self):
        return UserActivity.objects.filter(user=self.request.user)
