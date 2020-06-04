from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Очистка БД: профили пользователей'
    
    def handle(self, *args, **options):
        User.objects.all().delete()
        print('erasedb_users: OK')
