from django.core.management.base import BaseCommand

from forum.models import QuestionTag


class Command(BaseCommand):
    help = 'Заполнение БД: профили пользователей'
    
    def add_arguments(self, parser):
        parser.add_argument('count', type=int)
    
    def handle(self, *args, **options):
        for i in range(0, int(options['count'])):
            QuestionTag.objects.create(name='Tag' + str(i), description='This it description of tag number ' + str(i))
        print('filldb_questiontags: OK')
