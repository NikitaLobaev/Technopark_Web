from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from forum.models import Question, QuestionTag, Profile

# TODO: optimize and sort ALL imports EVERYWHERE!
questions_per_page = 3
users_per_page = 10


def questions_pagination(request, questions_):  # TODO: может быть, добавить limit на количество вопросов на странице
	order = request.GET.get('order')
	if order in Question.manager.accept_order:
		questions_ = questions_.order_by(order)
	paginator = Paginator(questions_, questions_per_page)
	try:
		page = paginator.page(request.GET.get('page', 1))
	except PageNotAnInteger:
		return HttpResponseNotFound()
	except EmptyPage:
		page = paginator.page(paginator.num_pages)
	return render(request, 'index.html', {
		'questions': page,
		'tags': QuestionTag.manager.all()
	})


def index(request):
	return questions_pagination(request, Question.manager)


@require_GET
def user(request, user_id):  # TODO: maybe rename "user" to "profile" everywhere
	try:
		profile_ = Profile.manager.get_by_id(user_id)
	except Question.DoesNotExist:
		return HttpResponseNotFound()
	return render(request, 'user.html', {
		'user': profile_,  # TODO: think about get_object_or_404(Profile, id=user_id) EVERYWHERE
		'tags': QuestionTag.manager.all()
	})


def users(request):
	paginator = Paginator(Profile.manager.all(), users_per_page)
	try:
		profiles = paginator.page(request.GET.get('page', 1))
	except PageNotAnInteger:
		return HttpResponseNotFound()
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
		'tags': QuestionTag.manager.all()
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
		tag_ = QuestionTag.manager.get_by_name(tag_name)
	except QuestionTag.DoesNotExist:
		return HttpResponseNotFound()
	return questions_pagination(request, Question.manager.get_by_tag(tag_))
