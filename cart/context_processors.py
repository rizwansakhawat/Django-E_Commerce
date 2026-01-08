from .models import Cart


def cart_context(request):
    """Inject cart item count (and items) for header dropdown, supporting guests and users."""
    item_count = 0
    cart_items = []

    try:
        # Ensure guests have a session so we can look up their cart
        if not request.user.is_authenticated and not request.session.session_key:
            request.session.save()

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).prefetch_related('items__product').first()
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key, user__isnull=True).prefetch_related('items__product').first() if session_key else None

        if cart:
            cart_items = list(cart.items.all())
            item_count = sum(i.quantity for i in cart_items)
    except Exception:
        cart_items = []

    return {
        'cart_item_count': item_count,
        'cart_items': cart_items,
    }
