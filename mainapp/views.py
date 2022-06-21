from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import os as os
from mainapp.models import Category, Product, Contacts
# from basketapp.models import Basket
from mainapp.services import get_basket, get_hot_product, get_same_product

# загрузка файла напрямую на сайт
# contact_file = 'contact.json'
# with open(os.path.join(os.getcwd(), contact_file)) as file:
#     contacts = json.load(file)


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
            products_list = Product.objects.filter(category__id=pk).\
                order_by('-price')

        page = request.GET.get('page')
        paginator = Paginator(products_list, 3)
        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'products': paginated_products,
            'category': category_item,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context)

    hot_product = get_hot_product()
    same_products = get_same_product(hot_product)
    context = {
        'title': title,
        'links_menu': links_menu,
        'basket': get_basket(request.user),
        'hot_product': hot_product,
        'same_products': same_products
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'продукт'
    links_menu = Category.objects.all()
    product_item = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'links_menu': links_menu,
        'product': product_item,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)
