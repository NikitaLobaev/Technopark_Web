from django.core.management.base import BaseCommand

from forum.models import User


class Command(BaseCommand):
	def handle(self, *args, **options):
		User.objects.create_user()
		print('OK')
