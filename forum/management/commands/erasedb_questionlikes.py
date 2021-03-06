from django.core.management.base import BaseCommand

from forum.models import Question, QuestionLike


class Command(BaseCommand):
    help = 'Очистка БД: рейтинги вопросов'
    
    def handle(self, *args, **options):
        QuestionLike.objects.all().delete()
        for question in Question.objects.all():
            question.rating = 0
            question.save()
        print('erasedb_questionlikes: OK')
