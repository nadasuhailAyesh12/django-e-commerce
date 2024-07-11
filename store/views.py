from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from category.models import Category
from .models import Product, Variation
from cart.models import CartItem
from cart.views import _get_session_id


class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_available=True).order_by('-created_at')
        category_slug = self.kwargs.get('category_slug')
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            queryset = queryset.filter(
                Q(name__icontains=keyword) | Q(description__icontains=keyword))
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        return queryset


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['product_slug'])
        in_cart = CartItem.objects.filter(
         product=product, cart__cart_id=_get_session_id(request))
        variationOBj = Variation.objects.filter(product=product)
        colors = [variation.variation_value for variation in variationOBj
                  if variation.variation_category == 'color']
        return render(request, 'store/product_detail.html',
                      {'product': product, 'in_cart': in_cart,
                       'colors': colors})
