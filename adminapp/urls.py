from django.urls import path
from adminapp import views as adminapp


app_name = 'adminapp'


urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.user_read, name='user_read'),
    path('users/update/<pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<pk>/', adminapp.user_delete, name='user_delete'),

    path('categories/create/', adminapp.category_create, name='category_create'),
    path('categories/read/', adminapp.category_read, name='category_read'),
    path('categories/update/<pk>/', adminapp.category_update, name='category_update'),
    path('categories/delete/<pk>/', adminapp.category_delete, name='category_delete'),

    path('categories/products/read/<pk>/', adminapp.products_read, name='products_read'),
    path('product/create/<pk>/', adminapp.product_create, name='product_create'),
    path('product/update/<pk>/', adminapp.product_update, name='product_update'),
    path('product/delete/<pk>/', adminapp.product_delete, name='product_delete'),
    path('product/detail/<pk>/', adminapp.product_delete, name='product_detail'),
]
