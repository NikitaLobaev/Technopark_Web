from django.core.management.base import BaseCommand

from forum.models import CommentToQuestion


class Command(BaseCommand):
	help = 'Очистка БД: комментарии к вопросам'
	
	def handle(self, *args, **options):
		CommentToQuestion.manager.all().delete()
		print("erasedb_commentstoquestion: OK")
