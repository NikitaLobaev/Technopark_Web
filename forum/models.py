from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.timezone import now


class MyUserManager(UserManager):
	def all(self):
		return self.filter(is_staff=False, is_active=True, is_superuser=False)


class User(AbstractUser):
	objects = MyUserManager()
	username = models.CharField(max_length=30, unique=True)
	email = models.EmailField(unique=True)
	avatar = models.ImageField(upload_to='avatar', default='/static/avatars/default.png')
	
	class Meta:
		ordering = ['username']
	
	def __str__(self):
		return self.username


class QuestionTag(models.Model):
	name = models.CharField('name', max_length=32, primary_key=True)
	description = models.TextField('description')
	
	class Meta:
		ordering = ['name']
	
	def __str__(self):
		return self.name


class QuestionManager(models.Manager):  # TODO: maybe place accept_order in model, not in manager
	accept_order = {
		'pub_date': '-pub_date',
		'rating': '-rating',
		'title': 'title'
	}
	
	def get_hot(self, min_rating):
		return self.filter(rating__gte=min_rating).order_by(self.accept_order['rating'])
	
	def get_by_tag(self, tag):
		return self.filter(tags__exact=tag)


class Question(models.Model):
	objects = QuestionManager()
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField('title', max_length=256)
	text = models.TextField('text')
	tags = models.ManyToManyField(QuestionTag)
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	answers_count = models.IntegerField('answers_count', default=0)
	rating = models.IntegerField('rating', default=0)
	
	class Meta:
		ordering = ['-pub_date']
	
	def get_title_short(self):
		if len(self.title) > 64:
			return self.title[:61] + '...'
		else:
			return self.title
	
	def get_text_short(self):
		if len(self.text) > 128:
			return self.text[:125] + '...'
		else:
			return self.text
	
	def get_comments(self):
		return CommentToQuestion.objects.get_by_question(question=self)
	
	def get_answers(self):
		return Answer.objects.get_by_question(question=self)


class AnswerManager(models.Manager):
	accept_order = {'pub_date': '-pub_date', 'rating': '-rating'}
	
	def get_by_question(self, question):
		return self.filter(question=question)


class Answer(models.Model):
	objects = AnswerManager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField('text')
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	rating = models.IntegerField('rating', default=0)
	
	def __str__(self):
		return self.text
	
	def get_comments(self):
		return CommentToAnswer.objects.get_by_answer(answer=self)


class Like(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	like = models.BooleanField('like', default=True)
	
	class Meta:
		abstract = True
	
	def __int__(self):
		if self.like:
			return 1
		else:
			return -1


class QuestionLike(Like):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerLike(Like):
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField('text', max_length=256)
	pub_date = models.DateTimeField('pub_date', default=now, blank=True)
	
	class Meta:
		abstract = True
	
	def __str__(self):
		return self.text


class CommentToQuestionManager(models.Manager):
	def get_by_question(self, question):
		return self.filter(question=question)


class CommentToQuestion(Comment):
	objects = CommentToQuestionManager()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['-pub_date']


class CommentToAnswerManager(models.Manager):
	def get_by_answer(self, answer):
		return self.filter(answer=answer)


class CommentToAnswer(Comment):
	objects = CommentToAnswerManager()
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['-pub_date']
