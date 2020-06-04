import random
from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Answer, AnswerLike, User


class Command(BaseCommand):
    help = 'Заполнение БД: рейтинг ответов'
    
    def add_arguments(self, parser):
        parser.add_argument('max_count', type=int)
    
    def handle(self, *args, **options):
        users = User.objects.all()
        for answer in Answer.objects.all():
            rating = 0
            for i in random.sample(range(len(users)), randrange(0, 1 + min(int(options['max_count']), len(users)))):
                like = randrange(0, 2) == 1
                if like:
                    rating = rating + 1
                else:
                    rating = rating - 1
                AnswerLike.objects.create(answer=answer, author=users[i], like=like)
            answer.rating = rating
            answer.save()
        print('filldb_answerlikes: OK')
