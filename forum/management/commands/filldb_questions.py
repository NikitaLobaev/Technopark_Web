from random import randrange, random

from django.core.management.base import BaseCommand

from forum.models import Profile, QuestionTag, Question


class Command(BaseCommand):
	help = 'Заполнение БД: вопросы'
	
	def add_arguments(self, parser):
		parser.add_argument('count', type=int)
	
	def handle(self, *args, **options):
		profiles = Profile.manager.all()
		question_tags = QuestionTag.manager.all()
		for i in range(0, int(options['count'])):
			question = Question.manager.create(author=profiles[randrange(0, len(profiles))],
					title="Title of " + str(i) + " question", text="This is the body of " + str(i) + " question!")
			for j in random.sample(range(0, len(question_tags)), 1 + randrange(0, len(question_tags))):
				question.tags.add(question_tags[j])
			question.save()
		print("filldb_questions: OK")
