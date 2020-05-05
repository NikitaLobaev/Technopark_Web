from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from forum.exceptions import QuestionNotFound, QuestionTagNotFound
from forum.models import Question, QuestionTag, Profile


def questions(request, questions_):
	order = request.GET.get('order', Question.manager.accept_order[0])
	page = request.GET.get('page', 1)
	if not Question.manager.check_order(order):  # защита от злоумышленников
		return HttpResponseBadRequest()
	questions_ = questions_.order_by(order)
	paginator = Paginator(questions_, 2)
	try:
		questions_ = paginator.page(page)
	except PageNotAnInteger:
		questions_ = paginator.page(1)
	except EmptyPage:
		questions_ = paginator.page(paginator.num_pages)
	return render(request, 'index.html', {
		'questions': questions_,
		'tags': QuestionTag.manager.get_all()
	})


def index(request):
	return questions(request, Question.manager)


def user(request, user_id):
	return render(request, 'user.html', {
		'user': Profile.manager.get_by_id(user_id),
		'tags': QuestionTag.manager.get_all()
	})


def users(request):
	order = request.GET.get('order', Question.manager.accept_order[0])
	page = request.GET.get('page', 1)
	if not Profile.manager.check_order(order):  # защита от злоумышленников
		return HttpResponseBadRequest()
	profiles_ = Profile.manager.order_by(order)
	paginator = Paginator(profiles_, 2)
	try:
		questions_ = paginator.page(page)
	except PageNotAnInteger:
		questions_ = paginator.page(1)
	except EmptyPage:
		questions_ = paginator.page(paginator.num_pages)
	return render(request, 'users.html', {
		'questions': questions_,
		'tags': QuestionTag.manager.get_all()
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
	return render(request, 'question.html', {
		'question': question_,
		'tags': QuestionTag.manager.get_all()
	})


def hot(request):
	return questions(request, Question.manager.get_hot_questions())


def tag(request, tag_name):
	try:
		questions_ = Question.manager.get_tag_questions(tag_name)
	except QuestionTagNotFound:
		return HttpResponseNotFound()
	return questions(request, questions_)
