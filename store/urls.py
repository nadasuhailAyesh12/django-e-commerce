from django.urls import path
from . import views

urlpatterns =[
path('',views.ProductListView.as_view(), name ='products_list'),
path('<slug:product_slug>/',views.ProductDetailView.as_view(), name ='product_details'),
path('category/<slug:category_slug>',views.ProductListView.as_view(), name ='products_by_category'),
]