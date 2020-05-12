from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from forum.models import Question, QuestionTag, Profile

# TODO: optimize and sort ALL imports EVERYWHERE!
questions_per_page = 3
users_per_page = 10


def questions_pagination(request, questions_):
	try:  # TODO: может быть, добавить limit на количество вопросов на странице
		order = Question.manager.accept_order[request.GET.get('order', next(iter(Question.manager.accept_order)))]
		paginator = Paginator(questions_.order_by(order), questions_per_page)
	except (KeyError, PageNotAnInteger):
		return HttpResponseNotFound()  # TODO: maybe raise Http404 instead?
	try:
		questions_ = paginator.page(request.GET.get('page', 1))
	except EmptyPage:
		questions_ = paginator.page(paginator.num_pages)
	return render(request, 'index.html', {
		'questions': questions_,
		'tags': QuestionTag.manager.all()
	})


def index(request):
	return questions_pagination(request, Question.manager)


@require_GET
def user(request, user_id):
	return render(request, 'user.html', {
		'user': get_object_or_404(Profile, id=user_id),
		'tags': QuestionTag.manager.all()
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
	return render(request, 'users.html', {
		'profiles': profiles,
		'tags': QuestionTag.manager.all()
	})


def ask(request):
	if request.user.is_authenticated:  # TODO: if not!!!
		return HttpResponseRedirect(reverse('forum:login'))
	return render(request, 'ask.html', {
		'tags': QuestionTag.manager.get_all()
	})


def question(request, question_id):
	try:
		question_ = Question.manager.get_by_id(question_id)
	except Question.DoesNotExist:
		return HttpResponseNotFound()
	return render(request, 'question.html', {
		'question': question_,
		'tags': QuestionTag.manager.all()
	})


def hot(request):
	return questions_pagination(request, Question.manager.get_hot())


def tag(request, tag_name):
	try:
		questions_ = Question.manager.get_by_tag(tag_name)
	except QuestionTag.DoesNotExist:
		return HttpResponseNotFound()
	return questions_pagination(request, questions_)
