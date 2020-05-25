from django.core.management.base import BaseCommand

from forum.models import AnswerLike, Answer


class Command(BaseCommand):
	help = 'Очистка БД: рейтинги ответов'
	
	def handle(self, *args, **options):
		AnswerLike.objects.all().delete()
		for answer in Answer.objects.all():
			answer.rating = 0
			answer.save()
		print('erasedb_answerlikes: OK')
