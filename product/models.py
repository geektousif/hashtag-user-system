from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    price = models.IntegerField()
    units_available = models.IntegerField()
    picture = models.ImageField(
        upload_to='images/product/', blank=True, null=True)

    def __str__(self):
        return self.title
