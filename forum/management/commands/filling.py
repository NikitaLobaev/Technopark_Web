from django.core.management.base import BaseCommand

from forum.models import Profile


class FillTestData(BaseCommand):
	help = 'Заполняет базу данных тестовыми данными'
	
	def add_arguments(self, parser):
		parser.add_argument('questions_count', type=int)
		parser.add_argument('answers_count', type=int)
	
	def handle(self, *args, **options):
		for n in range(100):
			usr1 = Profile.manager.create()
