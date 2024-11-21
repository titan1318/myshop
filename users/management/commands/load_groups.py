from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load predefined groups and permissions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading groups and permissions...")
        call_command('loaddata', 'groups.json')
        self.stdout.write(self.style.SUCCESS('Groups and permissions loaded successfully.'))
