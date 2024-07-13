from django.contrib import admin

from . import models


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "id",
        "name",
        "slug",
        "price",
        "stock",
        "is_available",
        "category",
        "updated_at",
    )


class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_editable = ("is_active",)
    list_filter = ("product", "variation_category", "variation_value")


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation, VariationAdmin)
