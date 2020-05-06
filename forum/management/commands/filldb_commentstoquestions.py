from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Profile, Question, CommentToQuestion


class Command(BaseCommand):
	help = 'Заполнение БД: комментарии к вопросам'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		for question in Question.manager.all():
			for i in range(0, randrange(0, int(options['max_count']))):
				CommentToQuestion.manager.create(author=profiles[randrange(0, len(profiles))], question=question,
						text="This is the comment to the question.").save()
		print("filldb_commentstoquestion: OK")
