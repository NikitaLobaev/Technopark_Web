from random import randrange

from django.core.management.base import BaseCommand

from forum.models import Profile, Question, Answer


class Command(BaseCommand):
	help = 'Заполнение БД: ответы'
	
	def add_arguments(self, parser):
		parser.add_argument('max_count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		for question in Question.manager.all():
			answers_count = randrange(0, min(int(options['max_count']), len(profiles)))
			for i in range(0, answers_count):
				Answer.manager.create(question=question, author=profiles[i],
						text="This is the answer to the question!").save()
			question.answers_count = answers_count
			question.save()
		print("filldb_answers: OK")
