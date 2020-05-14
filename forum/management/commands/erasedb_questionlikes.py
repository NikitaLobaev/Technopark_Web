from django.core.management.base import BaseCommand

from forum.models import QuestionLike


class Command(BaseCommand):
	help = 'Очистка БД: рейтинги вопросов'
	
	def handle(self, *args, **options):
		QuestionLike.objects.all().delete()
		print('erasedb_questionlikes: OK')
