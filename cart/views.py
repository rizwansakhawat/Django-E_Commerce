from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import get_object_or_404

from products.models import Product
from .models import Cart, CartItem


def _get_or_create_cart(request):
    user = request.user if request.user.is_authenticated else None

    if user:
        cart, _ = Cart.objects.get_or_create(user=user)
        # If session cart exists, merge it
        session_key = request.session.session_key
        if session_key:
            try:
                guest_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
                for item in guest_cart.items.select_related('product'):
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
                    if not created:
                        cart_item.quantity += item.quantity
                    cart_item.save()
                guest_cart.delete()
            except Cart.DoesNotExist:
                pass
        return cart

    # Guest cart by session
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key, user__isnull=True)
    return cart


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = quantity
    else:
        cart_item.quantity += quantity
    cart_item.save()

    messages.success(request, f'Added {product.name} to cart.')
    # Redirect back to product detail if referrer present, else home
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    return redirect(next_url or '/')


def cart_detail(request):
    cart = _get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all(),
    }
    return render(request, 'cart/checkout_cart.html', context)


@require_POST
def remove_from_cart(request):
    cart_item_id = request.POST.get('cart_item_id')
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'Removed {product_name} from cart.')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    return redirect(next_url or '/')

