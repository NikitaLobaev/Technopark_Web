from django.core.management.base import BaseCommand

from forum.models import QuestionLike, Question


class Command(BaseCommand):
	help = 'Очистка БД: рейтинги вопросов'
	
	def handle(self, *args, **options):
		QuestionLike.objects.all().delete()
		for question in Question.objects.all():
			question.rating = 0
		print('erasedb_questionlikes: OK')
