from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создает группу модераторов с соответствующими правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модераторы')
        permissions = [
            Permission.objects.get(codename='can_unpublish_product'),
            Permission.objects.get(codename='can_change_any_description'),
            Permission.objects.get(codename='can_change_any_category'),
        ]
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS('Группа модераторов успешно создана!'))
