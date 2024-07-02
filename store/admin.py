from django.contrib import admin
from . import models

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = ({'slug': ('name',)})
    list_display = ('name', 'slug', 'price', 'stock', 'is_available',
                    'category', 'updated_at')


admin.site.register(models.Product, ProductAdmin)
