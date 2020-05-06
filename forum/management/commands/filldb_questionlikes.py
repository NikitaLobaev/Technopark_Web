from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Profile, Question, QuestionLikes


class Command(BaseCommand):
	help = 'Заполнение БД: рейтинг вопросов'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		for question in Question.manager.all():
			rating = 0
			for i in range(0, randrange(0, min(len(profiles), int(options['max_count'])))):
				like = randrange(0, 2) == 1
				if like:
					rating = rating + 1
				else:
					rating = rating - 1
				QuestionLikes.objects.create(question=question, author=profiles[i], like=like).save()
			question.rating = rating
			question.save()
		print("filldb_questionlikes: OK")
