
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from products.models import Product
from .models import Cart, CartItem


def _get_or_create_cart(request):
    """Return a cart for the current user or session (guest)."""
    user = request.user if request.user.is_authenticated else None

    if user:
        cart, _ = Cart.objects.get_or_create(user=user)
        # Merge any guest cart tied to the same session
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


@method_decorator(require_POST, name='dispatch')
class AddToCartView(View):
    def post(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, "Please login to add items to cart.")
            # Redirect to login with the referring page as next
            next_url = request.META.get('HTTP_REFERER', 'products:index')
            return redirect(f"{'/account/login/'}?next={next_url}")
        
        # Prefer explicit product_id from POST; fallback to URL kwarg if ever used
        product_id = request.POST.get('product_id') or request.GET.get('product_id')
        cart = _get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        # Parse requested quantity (default to 1)
        raw_qty = request.POST.get('quantity', '1')
        try:
            quantity = int(str(raw_qty).strip())
            if quantity < 1:
                quantity = 1
        except (TypeError, ValueError):
            quantity = 1

        if created:
            item.quantity = quantity
        else:
            item.quantity += quantity
        item.save()

        messages.success(request, f"Added {product.name} to cart.")
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
        return redirect(next_url or 'cart:detail')


class CartDetailView(View):
    def get(self, request):
        cart = _get_or_create_cart(request)
        cart_items = cart.items.select_related('product').all()
        context = {
            'cart': cart,
            'cart_items': cart_items,
        }
        return render(request, 'cart/checkout_cart.html', context)


@method_decorator(require_POST, name='dispatch')
class RemoveFromCartView(View):
    def post(self, request):
        cart = _get_or_create_cart(request)
        cart_item_id = request.POST.get('cart_item_id')
        if not cart_item_id:
            messages.error(request, "Missing cart item id.")
            return redirect('cart:detail')

        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"Removed {product_name} from cart.")
        return redirect('cart:detail')


@method_decorator(require_POST, name='dispatch')
class UpdatecartItemQuantityView(View):
    def post(self, request, item_id, action):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if action == "increase":
            item.quantity += 1
            item.save()
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        return redirect('cart:detail')


@method_decorator(require_POST, name='dispatch')
class UpdateCartQuantityView(View):
    def post(self, request):
        """Update cart item quantity via AJAX. Expects JSON: {item_id: 123, quantity: 5}"""
        import json
        cart = _get_or_create_cart(request)
        
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = data.get('quantity', 1)
            
            # Validate quantity
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
            
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            # Check stock limit
            if quantity > cart_item.product.stock:
                quantity = cart_item.product.stock
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'item_id': item_id,
                'quantity': cart_item.quantity,
                'subtotal': float(cart_item.get_subtotal()),
                'cart_total': float(cart.get_total_price())
            })
        except (json.JSONDecodeError, ValueError, CartItem.DoesNotExist):
            return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
