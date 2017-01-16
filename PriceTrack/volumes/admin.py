from django.contrib import admin
from .models import Product, Retailer


# Register your models here.

class RetailerInLine(admin.StackedInline):
    model = Retailer


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        RetailerInLine,
    ]


admin.site.register(Product, ProductAdmin)
