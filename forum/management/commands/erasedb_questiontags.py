from django.core.management.base import BaseCommand

from forum.models import QuestionTag


class Command(BaseCommand):
    help = 'Очистка БД: теги вопросов'
    
    def handle(self, *args, **options):
        QuestionTag.objects.all().delete()
        print('erasedb_questiontags: OK')
