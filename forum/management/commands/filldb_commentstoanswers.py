from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Profile, CommentToAnswer, Answer


class Command(BaseCommand):
	help = 'Заполнение БД: комментарии к ответам'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		for answer in Answer.manager.all():
			for i in range(0, randrange(0, int(options['max_count']))):
				CommentToAnswer.manager.create(author=profiles[randrange(0, len(profiles))], answer=answer,
						text="This is the comment to the answer.").save()
		print("filldb_commenttoanswer: OK")
