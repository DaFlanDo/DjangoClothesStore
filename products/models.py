from django.db import models
from users.models import User


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name}"
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"Продукт: {self.name}|  Категория: {self.category.name}"


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(baskets.sum() for baskets in self)

    def total_quontity(self):
        return sum(baskets.quantity for baskets in self)


class Baskets(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.email}:{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

