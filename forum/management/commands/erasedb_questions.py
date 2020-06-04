from django.core.management.base import BaseCommand

from forum.models import Question


class Command(BaseCommand):
    help = 'Очистка БД: вопросы'
    
    def handle(self, *args, **options):
        Question.objects.all().delete()
        print('erasedb_questions: OK')
