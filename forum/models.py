from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now

from forum.exceptions import QuestionTagNotFound, QuestionNotFound, AnswerNotFound, ProfileNotFound


class ProfileManager(models.Manager):
	def get_by_id(self, profile_id):
		try:
			return self.get(id=profile_id)
		except ObjectDoesNotExist:
			raise ProfileNotFound()


class Profile(models.Model):
	manager = ProfileManager()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def get_user(self):
		return self.user
	
	def get_nickname(self):
		return self.get_user().username
	
	class Meta:
		ordering = ['user__username']


class QuestionTagManager(models.Manager):
	def get_by_name(self, name):
		try:
			return self.get(name=name)
		except ObjectDoesNotExist:
			raise QuestionTagNotFound()
	
	class Meta:
		ordering = ['name']


class QuestionTag(models.Model):
	manager = QuestionTagManager()
	name = models.CharField('name', max_length=32, primary_key=True)
	description = models.TextField('description')
	
	def get_name(self):
		return self.name
	
	def get_description(self):
		return self.description


class QuestionManager(models.Manager):
	accept_order = {'pub_date': '-pub_date', 'rating': '-rating', 'title': 'title'}
	
	def get_by_id(self, question_id):
		try:
			return self.get(id=question_id)
		except ObjectDoesNotExist:
			raise QuestionNotFound()
	
	def get_hot_questions(self):
		return self.filter(rating__gte=10).order_by(self.accept_order['rating'])
	
	def get_tag_questions(self, tag_name):
		return self.filter(tags__exact=QuestionTag.manager.get_by_name(tag_name))


class Question(models.Model):
	manager = QuestionManager()
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	title = models.CharField('title', max_length=256)
	text = models.TextField('text')
	tags = models.ManyToManyField(QuestionTag)
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	answers_count = models.IntegerField('answers_count', default=0)
	rating = models.IntegerField('rating', default=0)
	
	def get_author(self):
		return self.author
	
	def get_title(self):
		return self.title
	
	def get_title_short(self):
		t = self.get_title()
		if len(t) > 64:
			return t[:61] + '...'
		else:
			return t
	
	def get_text(self):
		return self.text
	
	def get_text_short(self):
		t = self.get_text()
		if len(t) > 128:
			return t[:125] + '...'
		else:
			return t
	
	def get_tags(self):
		return self.tags.all()
	
	def get_pub_date(self):
		return self.pub_date
	
	def get_comments(self):
		return CommentToQuestion.manager.get_by_question(question=self)
	
	def get_answers_count(self):
		return self.answers_count
	
	def get_answers(self):
		return Answer.manager.get_by_question(question=self)
	
	def get_rating(self):
		return self.rating


class QuestionLikes(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	like = models.BooleanField('like', default=True)
	
	def __int__(self):
		if self.like:
			return 1
		else:
			return -1


class CommentToQuestionManager(models.Manager):
	def get_by_question(self, question):
		return self.filter(question=question)


class CommentToQuestion(models.Model):
	manager = CommentToQuestionManager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	text = models.CharField('text', max_length=256)
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	
	def get_author(self):
		return self.author
	
	def get_text(self):
		return self.text
	
	def get_pub_date(self):
		return self.pub_date
	
	class Meta:
		ordering = ['-pub_date']


class AnswerManager(models.Manager):
	accept_order = {'pub_date': '-pub_date', 'rating': '-rating'}
	
	def get_by_id(self, answer_id):
		try:
			return self.get(id=answer_id)
		except ObjectDoesNotExist:
			raise AnswerNotFound()
	
	def get_by_question(self, question):
		return self.filter(question=question)


class Answer(models.Model):
	manager = AnswerManager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	text = models.TextField('text')
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	rating = models.IntegerField('rating', default=0)
	
	def get_author(self):
		return self.author
	
	def get_text(self):
		return self.text
	
	def get_pub_date(self):
		return self.pub_date
	
	def get_rating(self):
		return self.rating
	
	def get_comments(self):
		return CommentToAnswer.manager.get_by_answer(answer=self)


class AnswerLikes(models.Model):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	like = models.BooleanField('like', default=True)
	
	def __int__(self):
		if self.like:
			return 1
		else:
			return -1


class CommentToAnswerManager(models.Manager):
	def get_by_answer(self, answer):
		return self.filter(answer=answer)


class CommentToAnswer(models.Model):
	manager = CommentToAnswerManager()
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)
	text = models.CharField('text', max_length=256)
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	
	def get_author(self):
		return self.author
	
	def get_text(self):
		return self.text
	
	def get_pub_date(self):
		return self.pub_date
	
	class Meta:
		ordering = ['-pub_date']
