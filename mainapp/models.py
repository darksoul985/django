from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='название категории', max_length=64,
                            unique=True)
    description = models.TextField(verbose_name='краткое описание', blank=True)

    def __str__(self):
        return f'{self.pk} {self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='product', blank=True, verbose_name='Изображение')
    short_desc = models.CharField(max_length=256, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Contacts(models.Model):
    city = models.CharField(verbose_name='город', max_length=128, unique=True)
    address = models.CharField(verbose_name='адрес', max_length=254)
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(verbose_name='номер телефона', max_length=15)

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self):
        return f'{self.city} {self.address}'
