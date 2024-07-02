from django.views.generic import ListView
from store.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_available=True)
