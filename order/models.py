import uuid
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_init
from django.dispatch import receiver

from product.models import Product
from main.models import User
# Create your models here.


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        total = self.product.price * self.quantity
        self.price = total
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - {self.quantity} pieces"


STATUS_CHOICE = (
    ('pending', ' Pending'),
    ('delivered', 'Delivered')
)


class Order(models.Model):
    order_id = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField()
    order_items = models.ManyToManyField(OrderItem)
    total_price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICE,
                              max_length=20, default='pending')

    def __str__(self):
        return f"{self.user} - order ID: {self.order_id}"


@receiver(post_init, sender=Order)
def update_total_price(sender, instance, **kwargs):
    try:
        grand_total = 0
        # order_inst = Order.objects.get(pk=instance.pk)
        # print(instance)
        for item in instance.order_items.all():
            grand_total += item.price
        instance.total_price = grand_total
        print(instance.total_price)
        # print(order_inst)
    except Exception as e:
        print(e)
