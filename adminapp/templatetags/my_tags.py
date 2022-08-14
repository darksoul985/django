from django.conf import settings
from django import template


register = template.Library()


@register.filter(name='media_for_products')
def media_for_products(path_to_image):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not path_to_image:
        return f'{settings.STATIC_URL}img/default_product.jpg'

    return f'{settings.MEDIA_URL}{path_to_image}'


def media_for_users(path_to_image):
    """
    Автоматически добавляет относительный URL-путь к медиафайлам продуктов
    products_images/product1.jpg --> /media/products_images/product1.jpg
    """
    if not path_to_image:
        return f'{settings.STATIC_URL}img/default.jpg'

    return f'{settings.MEDIA_URL}{path_to_image}'


register.filter('media_for_users', media_for_users)
