from django.urls import path
import mainapp.views as mainapp

app_name = 'products'

urlpatterns = [
    path('', mainapp.products, name='hot_ptoducts'),
    path('<int:pk>/', mainapp.products_list, name='products_list'),
]
