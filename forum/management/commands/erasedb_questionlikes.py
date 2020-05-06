from django.core.management.base import BaseCommand

from forum.models import QuestionLikes


class Command(BaseCommand):
	help = 'Очистка БД: рейтинги вопросов'
	
	def handle(self, *args, **options):
		QuestionLikes.objects.all().delete()
		print("erasedb_questionlikes: OK")
