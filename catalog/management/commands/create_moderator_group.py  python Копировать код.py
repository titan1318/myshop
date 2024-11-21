from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Создание групп Модераторы и Контент-менеджеры с соответствующими правами'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана'))

        moderator_permissions = Permission.objects.filter(codename__in=[
            'can_unpublish_product',
            'can_change_any_description',
            'can_change_any_category'
        ])

        moderator_group.permissions.set(moderator_permissions)
        self.stdout.write(self.style.SUCCESS('Права добавлены в группу "Модераторы"'))
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджеры')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджеры" создана'))

        content_manager_permissions = Permission.objects.filter(codename='can_manage_blog')
        content_manager_group.permissions.set(content_manager_permissions)
        self.stdout.write(self.style.SUCCESS('Права добавлены в группу "Контент-менеджеры"'))
