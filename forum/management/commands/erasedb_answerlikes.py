from django.core.management.base import BaseCommand

from forum.models import AnswerLikes


class Command(BaseCommand):
	help = 'Очистка БД: рейтинги ответов'
	
	def handle(self, *args, **options):
		AnswerLikes.objects.all().delete()
		print("erasedb_answerlikes: OK")
