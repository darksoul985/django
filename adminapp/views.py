from django.shortcuts import render, get_object_or_404
from mainapp.models import Category, Product
from authapp.models import ShopUser
from adminapp.forms import UserAdminEditForm, ProductEditForm, CategoryEditForm
from authapp.forms import ShopUserRegisterForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
# from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin


class AccessMixin(UserPassesTestMixin):
    """
    переопределяем метод класса UserPassesTestMixin
    для проверки на суперпользователя
    """

    def test_func(self):
        return self.request.user.is_superuser


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


class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/user_list.html'
    paginate_by = 1

#  проверка на суперпользователя
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, *kwargs)


class UserUpdateView(AccessMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = UserAdminEditForm
    # success_url = reverse_lazy('adminapp:user_read')

    def get_success_url(self):
        return reverse('adminapp:user_update', args=[self.kwargs.get('pk')])


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


class CategoryCreateView(AccessMixin, CreateView):
    model = Category
    form_class = CategoryEditForm
    success_url = reverse_lazy('adminapp:category_read')
    template_name = 'adminapp/category_form.html'


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


# @user_passes_test(lambda u: u.is_superuser)
# def products_read(request, pk):
#     category_item = get_object_or_404(Category, pk=pk)
#     products_list = Product.objects.filter(category_id=pk)
#     context = {
#         'title': 'товары категории',
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products_list.html', context)
# class ProductListView(AccessMixin, ListView):
#     model = Product
#     template_name = 'adminapp/products_list.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(*args, *kwargs)
#         context_data['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
#         return context_data
#
#     def get_queryset(self):
#         return super().get_queryset().filter(category_id=self.kwargs.get('pk'))


class CategoryDetailView(AccessMixin, DetailView):
    model = Category
    template_name = 'adminapp/products_list.html'


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
        'form': product_form,
        'category': category_item
    }
    return render(request, 'adminapp/product_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    return None


class ProductDeleteView(AccessMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_delete_confirm.html'

    def get_success_url(self):
        category_pk = self.get_object().category_id
        return reverse('adminapp:products_read', args=[category_pk])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(AccessMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_info.html'
