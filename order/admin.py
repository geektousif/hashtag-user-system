from django.contrib import admin

from .models import Order, OrderItem
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['order_id']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
