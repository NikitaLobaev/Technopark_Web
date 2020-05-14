from random import randrange

from django.core.management.base import BaseCommand

from forum.models import User, Question, QuestionLike


class Command(BaseCommand):
	help = 'Заполнение БД: рейтинг вопросов'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		users = User.objects.all()
		for question in Question.objects.all():
			rating = 0
			for i in range(0, randrange(0, min(len(users), int(options['max_count'])))):
				like = randrange(0, 2) == 1
				if like:
					rating = rating + 1
				else:
					rating = rating - 1
				QuestionLike.objects.create(question=question, author=users[i], like=like)
			question.rating = rating
			question.save()
		print('filldb_questionlikes: OK')
