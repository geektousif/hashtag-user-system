from django.contrib import admin
from .models import Product, MultipleImage

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'title']


admin.site.register(Product, ProductAdmin)
admin.site.register(MultipleImage)
