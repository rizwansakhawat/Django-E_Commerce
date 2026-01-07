from .models import Cart


def cart_context(request):
    item_count = 0
    cart_items = []
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).prefetch_related('items__product').first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key, user__isnull=True).prefetch_related('items__product').first()
            else:
                cart = None

        if cart:
            cart_items = list(cart.items.all())
            item_count = sum(i.quantity for i in cart_items)
    except Exception:
        cart = None
        cart_items = []

    return {
        'cart_item_count': item_count,
        'cart_items': cart_items,
    }
