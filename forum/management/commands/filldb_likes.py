import random
from random import randrange

from django.core.management.base import BaseCommand, CommandError

from forum.models import Answer, AnswerLike, User, Question, QuestionLike


class Command(BaseCommand):
    help = 'Заполнение БД: рейтинг вопросов и ответов'
    
    def add_arguments(self, parser):
        parser.add_argument('questions_max_count', type=int)
        parser.add_argument('answers_max_count', type=int)
    
    def handle(self, *args, **options):
        questions_max_count = int(options['questions_max_count'])
        if questions_max_count < 0:
            raise CommandError('Параметр questions_max_count должен быть больше или равен 0.')
        answers_max_count = int(options['answers_max_count'])
        if answers_max_count < 0:
            raise CommandError('Параметр answers_max_count должен быть больше или равен 0.')
        users = User.objects.all()
        for state in [[Question.objects.all(), QuestionLike, min(questions_max_count, len(users)) + 1],
                      [Answer.objects.all(), AnswerLike, min(questions_max_count, len(users)) + 1]]:
            for object_ in state[0]:
                rating = 0
                for i in random.sample(range(len(users)), randrange(0, state[3])):
                    like = randrange(0, 2) == 1
                    if like:
                        rating += 1
                    else:
                        rating -= 1
                    state[1].objects.create(object_, users[i], like)
                object_.rating = rating
                object_.save()
        print('filldb_likes: OK')
