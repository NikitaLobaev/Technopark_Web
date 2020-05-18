from django.core.management.base import BaseCommand

from forum.models import User


class Command(BaseCommand):
	def handle(self, *args, **options):
		users = User.objects.all()
		users[2].avatar = '/media/default.png'
		print(users[2].username)
		users[2].save()
		#for user in users:
		#	user.avatar = '/static/default_avatar.png'
		print('OK')
