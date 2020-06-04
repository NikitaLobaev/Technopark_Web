from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Полная очистка БД'
    
    def handle(self, *args, **options):
        call_command('erasedb_questiontags')
        call_command('erasedb_users')
        print("erasedb: OK")
