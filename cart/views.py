from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from store.models import Product,Variation
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
    def match_variations(self, cart_item, product_variations):
        cart_item_variations = list(cart_item.variations.all())
        return set(cart_item_variations) == set(product_variations)

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        product_variations = []

        for item in request.POST:
            key = item
            if key != 'csrfmiddlewaretoken':
                value = request.POST[key].strip()
                variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                product_variations.append(variation)

        existing_cart_item = None
        cart, _ = Cart.objects.get_or_create(cart_id=_get_session_id(request))
        cart_items = CartItem.objects.filter(cart=cart, product=product)

        for cart_item in cart_items:
            if self.match_variations(cart_item, product_variations):
                existing_cart_item = cart_item
                break

        if existing_cart_item:
            if existing_cart_item.quantity < existing_cart_item.product.stock:
                existing_cart_item.quantity += 1
                existing_cart_item.save()

        else:
            new_cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=1
                )
            new_cart_item.variations.set(product_variations)  # Use .set() to assign variations

        return redirect('cart')


class decrementCartview(View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=self.kwargs['cart_item_id'])
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')


class incrementCartview(View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem,
                                      id=self.kwargs['cart_item_id'])
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('cart')


class remove_cart_item(View):
    def get(self, request, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=self.kwargs['cart_item_id'])
        cart_item.delete()
        return redirect('cart')
