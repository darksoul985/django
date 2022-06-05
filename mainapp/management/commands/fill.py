from django.core.management import BaseCommand
from django.conf import settings
from authapp.models import ShopUser
import json
from mainapp.models import Category, Product, Contacts


class Command(BaseCommand):

    @staticmethod
    def _load_data_from_file(file_name):
        with open(f'{settings.BASE_DIR}/mainapp/json/{file_name}.json') as file:
            return json.load(file)

    def handle(self, *args, **options):
        Category.objects.all().delete()

        categories_list = self._load_data_from_file('categories')
        categories_batch = []
        for cat in categories_list:
            categories_batch.append(
                Category(
                    name=cat.get('name'),
                    description=cat.get('description')
                )
            )

        Category.objects.bulk_create(categories_batch)

        Product.objects.all().delete()
        products_list = self._load_data_from_file('products')

        for prod in products_list:
            _cat = Category.objects.filter(name__icontains=prod.get('category')).first()
            prod['category'] = _cat

            Product.objects.create(**prod)

        shopuser = ShopUser.objects.create_superuser(
            username='django',
            email='django@bg.local',
            age=37
        )
        shopuser.set_password('geekbrains')
        shopuser.save()

        Contacts.objects.all().delete()
        contacts_list = self._load_data_from_file('contact_locations')

        for cont in contacts_list:
            Contacts.objects.create(**cont)
