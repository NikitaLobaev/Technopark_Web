from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from forum.exceptions import QuestionNotFound, QuestionTagNotFound
from forum.models import Question, QuestionTag, Profile

questions_per_page = 3
users_per_page = 10


def questions(request, questions_):
	order = request.GET.get('order')
	page = request.GET.get('page', 1)
	if order in Question.manager.accept_order:
		order = Question.manager.accept_order[order]
	else:
		order = Question.manager.accept_order[next(iter(Question.manager.accept_order))]
	paginator = Paginator(questions_.order_by(order), questions_per_page)
	try:
		questions_ = paginator.page(page)
	except PageNotAnInteger:
		questions_ = paginator.page(1)
	except EmptyPage:
		questions_ = paginator.page(paginator.num_pages)
	tags = QuestionTag.manager.all()
	return render(request, 'index.html', {
		'questions': questions_,
		'tags_left': tags[:int((len(tags) + 1) / 2)],
		'tags_right': tags[int((len(tags) + 1) / 2):]
	})


def index(request):
	return questions(request, Question.manager)


def user(request, user_id):
	tags = QuestionTag.manager.all()
	return render(request, 'user.html', {
		'user': Profile.manager.get_by_id(user_id),
		'tags_left': tags[:int((len(tags) + 1) / 2)],
		'tags_right': tags[int((len(tags) + 1) / 2):]
	})


def users(request):
	page = request.GET.get('page', 1)
	paginator = Paginator(Profile.manager.all(), users_per_page)
	try:
		profiles = paginator.page(page)
	except PageNotAnInteger:
		profiles = paginator.page(1)
	except EmptyPage:
		profiles = paginator.page(paginator.num_pages)
	tags = QuestionTag.manager.all()
	return render(request, 'users.html', {
		'profiles': profiles,
		'tags_left': tags[:int((len(tags) + 1) / 2)],
		'tags_right': tags[int((len(tags) + 1) / 2):]
	})


def ask(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse('forum:login'))
	return render(request, 'ask.html', {
		'tags': QuestionTag.manager.get_all()
	})


def question(request, question_id):
	try:
		question_ = Question.manager.get_by_id(question_id)
	except QuestionNotFound:
		return HttpResponseNotFound()
	tags = QuestionTag.manager.all()
	return render(request, 'question.html', {
		'question': question_,
		'tags_left': tags[:int((len(tags) + 1) / 2)],
		'tags_right': tags[int((len(tags) + 1) / 2):]
	})


def hot(request):
	return questions(request, Question.manager.get_hot_questions())


def tag(request, tag_name):
	try:
		questions_ = Question.manager.get_tag_questions(tag_name)
	except QuestionTagNotFound:
		return HttpResponseNotFound()
	return questions(request, questions_)
