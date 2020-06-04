from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Заполнение БД тестовыми данными'
	
	def handle(self, *args, **options):
		call_command('filldb_questiontags', 20)
		call_command('filldb_users', 100)
		call_command('filldb_questions', 1000)
		call_command('filldb_answers', 3)
		call_command('filldb_commentstoquestions', 2)
		call_command('filldb_commentstoanswers', 2)
		call_command('filldb_questionlikes', 30)
		call_command('filldb_answerlikes', 10)
		print('filldb: OK')
