from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Создаёт группы и назначает права'

    def handle(self, *args, **kwargs):
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')

        product_ct = ContentType.objects.get_for_model(Product)

        permissions = [
            Permission.objects.get(codename='change_product', content_type=product_ct),
            Permission.objects.get(codename='delete_product', content_type=product_ct),
            Permission.objects.get(codename='can_unpublish_product', content_type=product_ct),
        ]

        moderators_group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" успешно создана и права назначены.'))
