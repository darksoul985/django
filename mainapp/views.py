from django.shortcuts import render
import json
import os as os


contact_file = 'contact.json'
with open(os.path.join(os.getcwd(), contact_file)) as file:
    contacts = json.load(file)


def index(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    content = {
        'contact': contacts
    }
    return render(request, 'mainapp/contact.html', content)


def products(request):
    links_menu = [
        {'href': 'products_all', 'title': 'все'},
        {'href': 'products_home', 'title': 'дом'},
        {'href': 'products_office', 'title': 'офис'},
        {'href': 'products_modern', 'title': 'модерн'},
        {'href': 'products_classic', 'title': 'классика'},
    ]

    content = {
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)
