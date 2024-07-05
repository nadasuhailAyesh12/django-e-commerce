from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = ({'slug': ('name',)})
    list_display = ('id', 'name', 'slug', 'price', 'stock', 'is_available',
                    'category', 'updated_at')


admin.site.register(models.Product, ProductAdmin)
