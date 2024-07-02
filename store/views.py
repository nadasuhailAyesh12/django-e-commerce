from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from category.models import Category
from  .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        category_slug = self.kwargs.get('category_slug')

        if category_slug:
            category =get_object_or_404(Category, slug=category_slug)
            queryset = Product.objects.filter(category=category)
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'