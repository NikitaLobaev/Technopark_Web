from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from forum.forms import AskQuestionForm, SignupForm, LoginForm, EditAvatarForm, QuestionsPaginationForm
from forum.models import Question, QuestionTag, User

# TODO: optimize and sort ALL imports EVERYWHERE!
users_per_page = 10
hot_questions_min_rating = 10


def render_with_tags(request, template_name, context):
	context['tags'] = QuestionTag.objects.all()
	return render(request, template_name, context)


@require_GET
def render_questions(request, template_name, context):
	questions_pagination_form = QuestionsPaginationForm(request.GET)
	questions = context['questions']
	if questions_pagination_form.is_valid():
		paginator = Paginator(
			questions.order_by(questions_pagination_form.cleaned_data['order']),
			questions_pagination_form.cleaned_data['limit'])
		page = questions_pagination_form.cleaned_data['page']
	else:
		paginator = Paginator(questions, 10)
		page = 1
	try:
		context['questions'] = paginator.page(page)
	except PageNotAnInteger:
		return HttpResponseNotFound()
	except EmptyPage:
		context['questions'] = paginator.page(paginator.num_pages)
	context['questions_pagination_form'] = questions_pagination_form
	return render_with_tags(request, template_name, context)


@require_GET
def index(request):
	return render_questions(request, 'index.html', {
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
def profile(request):
	if request.method == 'POST':
		form = EditAvatarForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = EditAvatarForm()
	return render_with_tags(request, 'profile.html', {
		'form': form
	})


@login_required
def logout_(request):
	logout(request)
	return HttpResponseRedirect(request.GET.get('next', reverse('forum:index')))


@require_GET
def user(request, user_id):
	if user_id == request.user.id:
		return HttpResponseRedirect(reverse('forum:profile'))
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
	if request.method == 'POST':
		form = AskQuestionForm(request.POST)
		if form.is_valid():
			# question_ = form.save()
			question_ = Question.objects.create(
				author=request.user, title=form.cleaned_data['title'], text=form.cleaned_data['text'])
			question_.tags.set(form.cleaned_data['tags'])
			question_.save()
			return HttpResponseRedirect(reverse('forum:question', args=question_.id))
	else:
		form = AskQuestionForm()
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
