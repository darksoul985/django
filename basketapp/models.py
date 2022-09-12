from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='basket'
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

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    # @property
    def total_quantity(self):
        """
        return total quantity for user
        """
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    # @property
    def total_cost(self):
        """
        return total cost for user
        """
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()
        # return user.basket.select_related().order_by('product__category')

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
        ordering = ('created_at',)
