import os
import json
from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Очищает базу данных и заполняет её данными из фикстуры'

    def load_fixtures(self, file_path):
        abs_path = os.path.join(os.getcwd(), file_path)
        with open(abs_path, 'rb') as f:
            raw_data = f.read()
            print(raw_data)
        return json.loads(raw_data.decode('utf-8'))

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        data = self.load_fixtures('catalog/fixtures/catalog_data.json')

        for item in data:
            model = item['model']
            fields = item['fields']
            if model == 'catalog.category':
                Category.objects.create(**fields)
            elif model == 'catalog.product':
                category = Category.objects.get(pk=fields['category'])
                Product.objects.create(
                    name=fields['name'],
                    description=fields['description'],
                    price=fields['price'],
                    category=category,
                    available=fields['available']
                )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))
