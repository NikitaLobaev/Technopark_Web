import random
from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Answer, CommentToAnswer, User


class Command(BaseCommand):
    help = 'Заполнение БД: комментарии к ответам'
    
    def add_arguments(self, parser):
        parser.add_argument('max_count', type=int)
    
    def handle(self, *args, **options):
        users = User.objects.all()
        for answer in Answer.objects.all():
            for i in random.sample(range(len(users)), randrange(0, 1 + min(int(options['max_count']), len(users)))):
                CommentToAnswer.objects.create(
                    author=users[i], answer=answer, text='This is the comment to the answer.')
        print('filldb_commenttoanswer: OK')
