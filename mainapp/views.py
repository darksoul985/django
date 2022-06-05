from django.shortcuts import render, get_object_or_404
# import json
# import os as os
from mainapp.models import Category, Product, Contacts
from basketapp.models import Basket


# contact_file = 'contact.json'
# with open(os.path.join(os.getcwd(), contact_file)) as file:
#     contacts = json.load(file)

def get_basket(user):

    basket_list = []
    if user.is_authenticated:
        basket_list = sum(
            list(Basket.objects.filter(user=user).values_list('quantity', flat=True))
        )

    return basket_list


def main(request):
    title = 'главная'

    products = Product.objects.all()[:4]
    context = {
        'title': title,
        'products': products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def contact(request):
    contacts = Contacts.objects.all()

    context = {
        'contacts': contacts,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def products(request, pk=None):
    title = 'продукты'
    links_menu = Category.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'все', 'pk': 0}

        else:
            category_item = get_object_or_404(Category, pk=pk)
            products_list = Product.objects.filter(category__id=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': get_basket(request.user),
            'hot_product': Product.objects.all().order_by('?').first(),
            'same_products': Product.objects.all().order_by('?')[2:5]
        }

        return render(request, 'mainapp/products_list.html', context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'basket': get_basket(request.user),
        'hot_product': Product.objects.all().order_by('?').first(),
        'same_products': Product.objects.all().order_by('?')[2:5]
    }
    return render(request, 'mainapp/products.html', context)
