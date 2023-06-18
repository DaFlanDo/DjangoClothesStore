from django.contrib import admin
from products.models import ProductCategory, Product, Baskets

# Register your models here.
admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity','created_at')
    fields = ('name', 'category', 'price', 'quantity','image','description')


class BasketsAdmin(admin.TabularInline):
    model = Baskets
    fields = ('user', 'product','quantity','created_time' )
    readonly_fields = ('created_time',)
    extra = 0

