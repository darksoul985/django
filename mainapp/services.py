from mainapp.models import Product
from basketapp.models import Basket


def get_basket(user):

    basket_list = []
    if user.is_authenticated:
        basket_list = Basket.objects.filter(user=user)

    return basket_list


def get_hot_product():
    return Product.objects.all().order_by('?').first()


def get_same_product(product):
    return Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
