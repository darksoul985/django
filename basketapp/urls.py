from django.urls import path
import basketapp.views as basketapp


app_name = 'basket'

urlpatterns = [
    path('', basketapp.basket_list, name='list'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='remove'),
    path('edit/<int:pk>/<quantity>/', basketapp.basket_edit, name='edit'),
]
