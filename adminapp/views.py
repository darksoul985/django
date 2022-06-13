from django.shortcuts import render, get_object_or_404
from mainapp.models import Category, Product
from authapp.models import ShopUser
from adminapp.forms import UserAdminEditForm, ProductEditForm, CategoryEditForm
from authapp.forms import ShopUserRegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_read'))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': 'Создать пользователя',
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_read(request):
    context = {
        'title': 'админка/пользователи',
        'objects': ShopUser.objects.all().order_by(
            '-is_active',
            '-is_superuser'
        ),
    }
    print(context['objects'].all())
    return render(request, 'adminapp/user_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = UserAdminEditForm(
            request.POST,
            request.FILES,
            instance=user_item
        )

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(
                reverse('adminapp:user_update', args=[user_item.pk])
            )
    else:
        edit_form = UserAdminEditForm(instance=user_item)

    context = {
        'title': 'редактирование пользователя',
        'form': edit_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_item.is_active = False
        user_item.save()
        return HttpResponseRedirect(reverse('adminapp:user_read'))

    context = {
        'title': 'Удаление пользователя',
        'object': user_item
    }
    return render(request, 'adminapp/user_delete_confirm.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = CategoryEditForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_read'))
    else:
        category_form = CategoryEditForm()

    context = {
        'title': 'новая категория',
        'form': category_form
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_read(request):
    context = {
        'title': 'админ/категории',
        'objects': Category.objects.all().order_by('-is_active')
    }
    return render(request, 'adminapp/category_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    edit_category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_form = CategoryEditForm(
            request.POST,
            instance=edit_category
        )
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('adminapp:category_read'))
    else:
        category_form = CategoryEditForm(instance=edit_category)

    context = {
        'form': category_form,
        'title': 'редактирование категории'
    }
    return render(request, 'adminapp/category_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_item = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        if category_item.is_active:
            category_item.is_active = False
        else:
            category_item.is_active = True
        category_item.save()

        return HttpResponseRedirect(reverse('adminapp:category_read'))

    context = {
        'title': 'удаление категории',
        'object': category_item
    }
    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products_read(request, pk):
    category_item = get_object_or_404(Category, pk=pk)
    products_list = Product.objects.filter(category_id=pk)
    context = {
        'title': 'товары категории',
        'objects': products_list,
        'category': category_item
    }
    return render(request, 'adminapp/products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category_item = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)

        if product_form.is_valid():
            product_item = product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products_read', args=[product_item.category_id]))
    else:
        product_form = ProductEditForm()

    context = {
        'title': 'новый продукт',
        'form': product_form
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    return None


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    return None


@user_passes_test(lambda u: u.is_superuser)
def product_detail(request, pk):
    return None
