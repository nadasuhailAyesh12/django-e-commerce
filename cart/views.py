from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from store.models import Product
from cart.models import CartItem, Cart


def _get_session_id(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key


class CartListView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.filter(
            cart_id=_get_session_id(self.request)).first()
        if (cart):
            cartItems = cart.cartitem_set.filter(is_active=True)
            if (not cartItems.exists()):
                cartItems = []
                totalPrice = 0
                tax = 0
                grandTotal = 0
            else:
                totalPrice = sum(
                    item.product.price * item.quantity for item in cartItems)
                tax = (2 * totalPrice) / 100
                grandTotal = tax + totalPrice
        else:
            cartItems = []

        context = {
            'cartItems': cartItems,
            'totalPrice': totalPrice,
            'tax': tax,
            'grandTotal': grandTotal,
            }
        return render(request, 'store/cart.html', context)


class AddCartView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        cart, _ = Cart.objects.get_or_create(cart_id=_get_session_id(request))
        cartItem, created = CartItem.objects.get_or_create(
            cart=cart, product=product)
        if not created:
            if cartItem.quantity < cartItem.product.stock:
                cartItem.quantity += 1
                cartItem.save()
        return redirect('cart')


class decrementCartview(View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=self.kwargs['cart_item_id'])
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')


class remove_cart_item(View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=self.kwargs['cart_item_id'])
        cart_item.delete()
        return redirect('cart')
