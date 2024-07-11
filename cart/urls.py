from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartListView.as_view(), name='cart'),
    path("<int:product_id>/", views.AddCartView.as_view(), name='add_cart'),
    path("cartItem/<int:cart_item_id>", views.remove_cart_item.as_view(),
         name='remove_cart_item'),
    path("increment/<int:cart_item_id>", views.incrementCartview.as_view(),
         name='increment_cart'),
    path("decrement/<int:cart_item_id>", views.decrementCartview.as_view(),
         name='decrement_cart')
]
