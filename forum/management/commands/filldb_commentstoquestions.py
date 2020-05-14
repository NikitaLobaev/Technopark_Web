import random
from random import randrange

from django.core.management.base import BaseCommand

from forum.models import User, Question, CommentToQuestion


class Command(BaseCommand):
	help = 'Заполнение БД: комментарии к вопросам'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		users = User.objects.all()
		for question in Question.objects.all():
			for i in random.sample(range(len(users)), randrange(0, 1 + min(int(options['max_count']), len(users)))):
				CommentToQuestion.objects.create(
					author=users[i], question=question, text='This is the comment to the question.')
		print('filldb_commentstoquestion: OK')
