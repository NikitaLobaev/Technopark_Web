from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from forum.forms import AskQuestionForm, SignupForm, LoginForm
from forum.models import Question, QuestionTag, User

# TODO: optimize and sort ALL imports EVERYWHERE!
questions_per_page = 5
users_per_page = 10
hot_questions_min_rating = 10


def render_with_tags(request, template_name, context):
	context['tags'] = QuestionTag.objects.all()
	return render(request, template_name, context)


@require_GET  # TODO: может быть, добавить limit на количество вопросов на странице
def render_questions(request, template_name, context):
	order = request.GET.get('order')
	if order in Question.objects.accept_order:
		context['questions'] = context['questions'].order_by(Question.objects.accept_order[order])
	paginator = Paginator(context['questions'], questions_per_page)
	try:
		context['questions'] = paginator.page(request.GET.get('page', 1))
	except PageNotAnInteger:
		return HttpResponseNotFound()
	except EmptyPage:
		context['questions'] = paginator.page(paginator.num_pages)
	return render_with_tags(request, template_name, context)


@require_GET
def index(request):
	return render_questions(request, 'questions.html', {
		'questions': Question.objects.all()
	})


def signup(request):  # TODO: при смене пароля запрашивать его заново в целях безопасности
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('forum:index'))
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			if not User.objects.filter(username=form.cleaned_data['username']).exists():
				user_ = form.save()
				login(request, user_)
				return HttpResponseRedirect(request.GET.get('next', reverse('forum:index')))
			form.add_error('username', 'Пользователь с таким никнеймом уже зарегистрирован.')
	else:
		form = SignupForm()
	return render_with_tags(request, 'signup.html', {
		'form': form
	})


def login_(request):  # TODO: captcha EVERYWHERE if it needs!
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('forum:index'))
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user_ = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user_:
				login(request, user_)
				return HttpResponseRedirect(request.GET.get('next', reverse('forum:profile_edit')))
			else:
				form.add_error('username', 'Неверный логин или пароль')
	else:
		form = LoginForm()
	return render_with_tags(request, 'login.html', {
		'form': form
	})


@login_required
def profile_edit(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user_ = form.save()
			User.objects.create(user=user_)
			login(request, user_)
			return HttpResponseRedirect(request.GET.get('next', reverse('forum:index')))
	else:
		form = SignupForm()
	return render_with_tags(request, 'profile_edit.html', {
		'form': form
	})


@login_required
def logout_(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('next', reverse('forum:index')))


@require_GET
def user(request, user_id):
	return render_with_tags(request, 'user.html', {
		'user': get_object_or_404(User, id=user_id)
	})


@require_GET
def users(request):
	paginator = Paginator(User.objects.all(), users_per_page)
	try:
		users_ = paginator.page(request.GET.get('page', 1))
	except PageNotAnInteger:
		return HttpResponseNotFound()
	except EmptyPage:
		users_ = paginator.page(paginator.num_pages)
	return render_with_tags(request, 'users.html', {
		'users': users_
	})


@login_required
def ask(request):
	form = AskQuestionForm(request.user, request.POST)
	if form.is_valid():
		question_ = form.save()
		return HttpResponseRedirect(reverse('forum:question', args=question_.id))
	return render_with_tags(request, 'ask.html', {
		'form': form
	})


def question(request, question_id):
	return render_with_tags(request, 'question.html', {
		'question': get_object_or_404(Question, id=question_id)
	})


@require_GET
def hot(request):
	return render_questions(request, 'hot.html', {
		'questions': Question.objects.get_hot(hot_questions_min_rating)
	})


@require_GET
def tag(request, tag_name):
	return render_questions(request, 'tag.html', {
		'tag_name': tag_name,
		'questions': Question.objects.get_by_tag(get_object_or_404(QuestionTag, name=tag_name))
	})
