from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from category.models import Category
from .models import Product
from cart.models import CartItem
from cart.views import _get_session_id


class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = Product.objects.filter(category=category)
        return queryset


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        in_cart = CartItem.objects.filter(
         product=product, cart__cart_id=_get_session_id(request))
        return render(request, 'store/product_detail.html',
                      {'product': product, 'in_cart': in_cart})
