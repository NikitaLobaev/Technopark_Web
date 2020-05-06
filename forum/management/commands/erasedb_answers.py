from django.core.management.base import BaseCommand

from forum.models import Answer


class Command(BaseCommand):
	help = 'Очистка БД: ответы'
	
	def handle(self, *args, **options):
		Answer.manager.all().delete()
		print("erasedb_answers: OK")
