from django.contrib import admin
from authapp.models import ShopUser

@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active')
    list_filter = ('is_active',)
