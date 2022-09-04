from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"                                       #to return the name in " 's " format

class Product(models.Model):
    main_image = models.ImageField(upload_to="Product")
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=200, verbose_name='Preview Text')
    details_text = models.TextField(max_length=1000, verbose_name='Details Text')
    price = models.IntegerField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created',]                                                  #to show the products in descending order
