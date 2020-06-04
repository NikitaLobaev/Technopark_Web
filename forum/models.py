import os
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import now


class MyUserManager(UserManager):
    def all(self):
        return self.filter(is_staff=False, is_active=True, is_superuser=False)
    
    def get_top(self, count):
        return self.annotate(
            rating=Count(Question, filter=Q(question__pub_date__gt=now() - timedelta(days=90)))).order_by('-rating')[
        :count]


def upload_avatar_filename(instance, filename):  # TODO: возможно переделать
    return os.path.join('avatar', str(instance.id) + '_' + filename)


class User(AbstractUser):
    objects = MyUserManager()
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(default='avatar/default.png', upload_to=upload_avatar_filename)
    questions_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-answers_count']
    
    def __str__(self):
        return self.username
    
    def question_added(self):
        self.questions_count += 1
        self.save()
    
    def answer_added(self, question):
        question.answers_count += 1
        question.save()
        self.answers_count += 1
        self.save()


class QuestionTagManager(models.Manager):
    def get_top(self, count):
        return self.annotate(
            rating=Count(Question, filter=Q(question__pub_date__gt=now() - timedelta(days=90)))).order_by('-rating')[
        :count]


class QuestionTag(models.Model):
    objects = QuestionTagManager()
    name = models.CharField(max_length=32, primary_key=True)
    description = models.TextField('description')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_top(self, min_rating):
        return self.filter(rating__gte=min_rating)
    
    def get_by_tag(self, tag):
        return self.filter(tags__exact=tag)


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(QuestionTag)
    pub_date = models.DateTimeField(default=now, blank=True)
    answers_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    
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
    
    def was_rated(self, user):
        return QuestionLike.objects.filter(author=user, question=self)
    
    def rating_add(self, user, like):
        like = QuestionLike.objects.create(author=user, like=like, question=self)
        if like:
            self.rating = self.rating + 1
        else:
            self.rating = self.rating - 1
        self.save()
    
    def rating_remove(self, user):
        like = QuestionLike.objects.get(author=user, question=self)
        if like.like:
            self.rating = self.rating - 1
        else:
            self.rating = self.rating + 1
        like.delete()
        self.save()


class AnswerManager(models.Manager):
    def get_by_question(self, question):
        return self.filter(question=question)


class Answer(models.Model):
    objects = AnswerManager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=now, blank=True)
    rating = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-rating']
    
    def __str__(self):
        return self.text
    
    def get_comments(self):
        return CommentToAnswer.objects.get_by_answer(answer=self)


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
    
    class Meta:  # TODO
        abstract = True
        unique_together = ('author', 'like')
    
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
    text = models.CharField(max_length=256)
    pub_date = models.DateTimeField(default=now, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['-pub_date']
    
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
