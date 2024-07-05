from .models import CartItem, Cart
from .views import _get_session_id


def cart_count(request):
    try:
        cart_id = _get_session_id(request)
        cart = Cart.objects.filter(cart_id=cart_id).first()
        cart_count = CartItem.objects.filter(cart=cart).count()
    except Cart.DoesNotExist:
        cart_count = 0
    return {'cart_count': cart_count}
