from django.shortcuts import render
import json
import os as os
from .models import Category, Product


contact_file = 'contact.json'
with open(os.path.join(os.getcwd(), contact_file)) as file:
    contacts = json.load(file)


def main(request):
    title = 'главная'

    products = Product.objects.all()[:4]
    content = {
        'title': title,
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {
        'contact': contacts
    }
    return render(request, 'mainapp/contact.html', content)


def products(request):
    content = {
        'links_menu': Category.objects.all()
    }
    return render(request, 'mainapp/products.html', content)


def products_list(request, pk):
    print(request.resolver_match)
    content = {
        'links_menu': Category.objects.all()
    }
    return render(request, 'mainapp/products.html', content)
