import random
from random import randrange

from django.core.management.base import BaseCommand

from forum.models import User, QuestionTag, Question


class Command(BaseCommand):
	help = 'Заполнение БД: вопросы'
	
	def add_arguments(self, parser):
		parser.add_argument('count', type=int)
	
	def handle(self, *args, **options):
		users = User.objects.all()
		question_tags = QuestionTag.objects.all()
		for i in range(0, int(options['count'])):
			question = Question.objects.create(
				author=users[randrange(0, len(users))], title='Title of ' + str(i) + ' question',
				text='This is the body of ' + str(i) + ' question!')
			for j in random.sample(range(len(question_tags)), randrange(1, min(len(question_tags), 5))):
				question.tags.add(question_tags[j])
			question.save()
		print('filldb_questions: OK')
