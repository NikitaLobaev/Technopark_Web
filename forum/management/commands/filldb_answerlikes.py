from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Profile, Answer, AnswerLikes


class Command(BaseCommand):
	help = 'Заполнение БД: рейтинг ответов'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		for answer in Answer.manager.all():
			rating = 0
			for i in range(0, randrange(0, min(len(profiles), int(options['max_count'])))):
				like = randrange(0, 2) == 1
				if like:
					rating = rating + 1
				else:
					rating = rating - 1
				AnswerLikes.objects.create(answer=answer, author=profiles[i], like=like).save()
			answer.rating = rating
			answer.save()
		print("filldb_answerlikes: OK")
