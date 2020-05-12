from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from forum.models import Profile


class Command(BaseCommand):
	help = 'Заполнение БД: профили пользователей'
	
	def add_arguments(self, parser):
		parser.add_argument('count', type=int)
	
	def handle(self, *args, **options):
		for i in range(0, int(options['count'])):
			user = User.objects.create_user(username="User" + str(i), email="email" + str(i) + "@mail.ru",
					password="abracadabra")
			Profile.manager.create(user=user)
		print("filldb_profiles: OK")
