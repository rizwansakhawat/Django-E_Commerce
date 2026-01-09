from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from decimal import Decimal
from cart.views import _get_or_create_cart
from .forms import ShippingForm, PaymentForm
from .models import Order, OrderItem, Payment, OrderTracker
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.

def checkout_info(request):
    """Checkout shipping information page"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')
    
    # Get user's saved addresses if authenticated
    saved_addresses = []
    if request.user.is_authenticated:
        from accounts.models import Address
        saved_addresses = Address.objects.filter(
            user=request.user, 
            is_active=True
        ).order_by('-is_default', '-created_at')
    
    # Pre-fill form with any saved session data and user profile
    session_data = request.session.get('shipping_info', {}) or {}
    initial_data = dict(session_data)
    if request.user.is_authenticated:
        user = request.user
        initial_data.setdefault('first_name', user.first_name or '')
        initial_data.setdefault('last_name', user.last_name or '')
        initial_data.setdefault('email', user.email or '')
    initial_data.setdefault('country', 'Pakistan')

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            request.session['shipping_info'] = form.cleaned_data
            messages.success(request, 'Shipping information saved.')
            return redirect('orders:checkout_payment')
        shipping_data = form.data
    else:
        form = ShippingForm(initial=initial_data)
        shipping_data = form.initial
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_data': shipping_data,
        'form': form,
        'saved_addresses': saved_addresses,
    }
    return render(request, 'orders/checkout_info.html', context)


def checkout_payment(request):
    """Checkout payment page"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.select_related('product').all()
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')
    
    # Check stock availability before proceeding
    out_of_stock_items = []
    for item in cart_items:
        if item.product.stock < item.quantity:
            out_of_stock_items.append(f"{item.product.name} (Available: {item.product.stock}, Requested: {item.quantity})")
    
    if out_of_stock_items:
        for item_msg in out_of_stock_items:
            messages.error(request, f'Insufficient stock: {item_msg}')
        return redirect('cart:detail')
    
    # Get shipping info from session
    shipping_info = request.session.get('shipping_info', {})
    
    if not shipping_info:
        messages.warning(request, 'Please complete shipping information first.')
        return redirect('orders:checkout_info')
    
    # Handle POST - Stripe payment processing
    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')
        
        if not payment_intent_id:
            messages.error(request, 'Payment failed. Please try again.')
            return render(request, 'orders/checkout_payment.html', {
                'cart': cart,
                'cart_items': cart_items,
                'shipping_info': shipping_info,
                'form': PaymentForm(),
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'error': 'Payment processing failed'
            })
        
        try:
            # Verify payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                # Payment successful - create Order and related records, then save info to session
                shipping = shipping_info
                email = request.POST.get('email') or (request.user.email if request.user.is_authenticated else None)

                # Fallback to prevent nulls; ideally email is provided on payment page
                if not email:
                    email = 'customer@example.com'

                subtotal = Decimal(str(cart.get_total_price()))
                shipping_cost = Decimal('0.00')
                tax = Decimal('0.00')
                total_amount = subtotal + shipping_cost + tax

                # Generate unique order number
                order_number = f"ORD-{timezone.now().strftime('%Y%m%d%H%M%S')}-{cart.id}"

                # Compose phone from area_code + primary_phone
                phone = f"({shipping.get('area_code', '')}) {shipping.get('primary_phone', '')}".strip()

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    order_number=order_number,
                    first_name=shipping.get('first_name', ''),
                    last_name=shipping.get('last_name', ''),
                    email=email,
                    phone=phone,
                    shipping_address=shipping.get('address_1', ''),
                    shipping_city=shipping.get('city', ''),
                    shipping_state=shipping.get('state', ''),
                    shipping_postal_code=shipping.get('zip_code', ''),
                    shipping_country=shipping.get('country', ''),
                    billing_address=shipping.get('address_1', ''),
                    billing_city=shipping.get('city', ''),
                    billing_state=shipping.get('state', ''),
                    billing_postal_code=shipping.get('zip_code', ''),
                    billing_country=shipping.get('country', ''),
                    order_status='processing',
                    payment_status='completed',
                    payment_method='Stripe',
                    subtotal=subtotal,
                    shipping_cost=shipping_cost,
                    tax=tax,
                    total_amount=total_amount,
                )

                # Create order items and decrease product stock
                for ci in cart.items.select_related('product').all():
                    OrderItem.objects.create(
                        order=order,
                        product=ci.product,
                        quantity=ci.quantity,
                        unit_price=Decimal(str(ci.get_unit_price())),
                        subtotal=Decimal(str(ci.get_subtotal())),
                    )
                    
                    # Decrease product stock
                    product = ci.product
                    product.stock -= ci.quantity
                    
                    # Mark as unavailable if stock reaches 0
                    if product.stock <= 0:
                        product.stock = 0
                        product.is_available = False
                    
                    product.save(update_fields=['stock', 'is_available'])

                # Create payment record
                Payment.objects.create(
                    order=order,
                    payment_method='stripe',
                    stripe_payment_intent_id=payment_intent_id,
                    stripe_client_secret=intent.client_secret,
                    stripe_charge_id=None,
                    stripe_status='succeeded',
                    amount=total_amount,
                    currency='USD',
                    transaction_id=payment_intent_id,
                    receipt_url=None,
                    paid_at=timezone.now(),
                )

                # Add initial tracker status
                OrderTracker.objects.create(
                    order=order,
                    status='order_placed',
                    description='Order placed and payment confirmed via Stripe.'
                )

                # Snapshot cart items for the completion page before clearing
                items_snapshot = []
                for item in cart.items.select_related('product').all():
                    items_snapshot.append({
                        'name': item.product.name,
                        'quantity': item.quantity,
                        'unit_price': float(item.get_unit_price()),
                        'subtotal': float(item.get_subtotal()),
                    })
                request.session['completed_items'] = items_snapshot
                request.session['completed_total'] = float(cart.get_total_price())
                request.session['order_number'] = order.order_number

                # Clear cart items after successful payment
                cart.items.all().delete()

                request.session['payment_info'] = {
                    'payment_intent_id': payment_intent_id,
                    'amount': intent.amount,
                    'status': intent.status,
                    'payment_type': 'Stripe'
                }
                messages.success(request, 'Payment successful!')
                return redirect('orders:checkout_complete')
            else:
                messages.error(request, f'Payment status: {intent.status}')
                return render(request, 'orders/checkout_payment.html', {
                    'cart': cart,
                    'cart_items': cart_items,
                    'shipping_info': shipping_info,
                    'form': PaymentForm(),
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                    'error': 'Payment not completed'
                })
                
        except stripe.error.StripeError as e:
            messages.error(request, f'Payment error: {str(e)}')
            return render(request, 'orders/checkout_payment.html', {
                'cart': cart,
                'cart_items': cart_items,
                'shipping_info': shipping_info,
                'form': PaymentForm(),
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'error': str(e)
            })
    
    # GET - Display payment form
    # Calculate total
    total_amount = int(cart.get_total_price() * 100)  # Convert to cents
    
    try:
        # Create Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency='usd',
            metadata={
                'cart_id': cart.id,
                'user_id': request.user.id if request.user.is_authenticated else 'anonymous'
            }
        )
        client_secret = intent.client_secret
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('cart:detail')
    
    form = PaymentForm()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_info': shipping_info,
        'form': form,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret,
    }
    return render(request, 'orders/checkout_payment.html', context)


def checkout_complete(request):
    """Checkout completion page"""
    # Get saved info from session
    shipping_info = request.session.get('shipping_info', {})
    payment_info = request.session.get('payment_info', {})
    cart = _get_or_create_cart(request)
    completed_items = request.session.get('completed_items', [])
    completed_total = request.session.get('completed_total')
    order_number = request.session.get('order_number')
    
    context = {
        'shipping_info': shipping_info,
        'payment_info': payment_info,
        'cart': cart,
        'completed_items': completed_items,
        'completed_total': completed_total,
        'order_number': order_number,
    }
    
    # Clear session data after viewing completion
    if 'shipping_info' in request.session:
        del request.session['shipping_info']
    if 'payment_info' in request.session:
        del request.session['payment_info']
    if 'completed_items' in request.session:
        del request.session['completed_items']
    if 'completed_total' in request.session:
        del request.session['completed_total']
    if 'order_number' in request.session:
        del request.session['order_number']
    
    return render(request, 'orders/checkout_complete.html', context)
