from django.db import models
from django.conf import settings

from App_Shop.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name = "cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.item}"

    def get_total(self):
        total = self.item.price * self.quantity
        # float_total = format(total, '0.2f')
        # return float_total
        return total

class Order(models.Model):
    order_items = models.ManyToManyField(Cart)                                           #user can choose multiple amount of same item i.e 'ManyToMany'
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_Id = models.CharField(max_length=264, blank=True,null=True)
    Order_Id = models.CharField(max_length=264, blank=True, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            total += int(order_item.get_total())
        return total
