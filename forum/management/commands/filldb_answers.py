import random
from random import randrange

from django.core.management.base import BaseCommand

from forum.models import User, Question, Answer


class Command(BaseCommand):
	help = 'Заполнение БД: ответы'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)  # максимальное количество ответов на каждый вопрос
	
	def handle(self, *args, **options):
		users = User.objects.all()
		for question in Question.objects.all():
			answers_count = randrange(0, 1 + min(int(options['max_count']), len(users)))
			for i in random.sample(range(len(users)), answers_count):
				answer = Answer.objects.create(question=question, author=users[i], text='This is the answer to the question!')
				answer.author.answer_added(question)
			question.answers_count = answers_count
			question.save()
		print('filldb_answers: OK')
