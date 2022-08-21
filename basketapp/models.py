from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлен'
    )

    def __str__(self):
        return f'{self.product}, {self.quantity}'

    @property
    def product_cost(self):
        """
        return cost of all products this type
        """
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        """
        return total quantity for user
        """
        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        """
        return total cost for user
        """
        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        ordering = ('created_at',)
