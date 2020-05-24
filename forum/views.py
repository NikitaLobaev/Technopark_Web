from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from forum.forms import AskQuestionForm, SignupForm, LoginForm, EditProfileForm, \
	EditPasswordForm, AnswerTheQuestionForm, CommentToQuestionForm, QuestionRatingForm, PaginationForm
from forum.models import Question, QuestionTag, User

# TODO: optimize and sort ALL imports EVERYWHERE!
# TODO: бизнес-логика сохранения форм тоже вероятно надо перенести в models
hot_questions_min_rating = 10


def render_with_tags(request, template_name, context):
	context['tags'] = QuestionTag.objects.all()
	return render(request, template_name, context)


@require_GET
def render_questions(request, template_name, context):
	if request.GET:
		questions_pagination_form = PaginationForm(request.GET)
	else:
		questions_pagination_form = PaginationForm()
	questions = context['pagination']
	if questions_pagination_form.is_valid():
		paginator = Paginator(
			questions.order_by(questions_pagination_form.cleaned_data['order']),
			questions_pagination_form.cleaned_data['limit'])
		page = questions_pagination_form.cleaned_data['page']
	else:
		paginator = Paginator(questions, 10)
		page = 1
	try:
		context['pagination'] = paginator.page(page)
	except PageNotAnInteger:
		return HttpResponseNotFound()
	except EmptyPage:
		context['pagination'] = paginator.page(paginator.num_pages)
	context['pagination_form'] = questions_pagination_form
	return render_with_tags(request, template_name, context)


@require_GET
def index(request):
	return render_questions(request, 'index.html', {
		'pagination': Question.objects.all()
	})


def signup(request):  # TODO: при смене пароля запрашивать его заново в целях безопасности
	if request.user.is_authenticated:
		return redirect('forum:index')
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			if not User.objects.filter(username=form.cleaned_data['username']).exists():
				user_ = form.save()
				login(request, user_)
				return redirect(request.GET.get('next', reverse('forum:index')))
			form.add_error('username', 'Пользователь с таким никнеймом уже зарегистрирован.')
	else:
		form = SignupForm()
	return render_with_tags(request, 'signup.html', {
		'form': form
	})


def login_(request):  # TODO: captcha EVERYWHERE if it needs!
	if request.user.is_authenticated:
		return redirect('forum:index')
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		if form.is_valid():
			user_ = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user_:
				login(request, user_)
				return redirect(request.GET.get('next', reverse('forum:index')))
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
		edit_profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
		edit_password_form = EditPasswordForm(data=request.POST, user=request.user)
		if edit_profile_form.is_valid():
			x = edit_profile_form.save()
		elif edit_password_form.is_valid():
			edit_password_form.save()
	else:
		edit_profile_form = EditProfileForm(instance=request.user)
		edit_password_form = EditPasswordForm(user=request.user)
	return render_with_tags(request, 'profile.html', {
		'edit_profile_form': edit_profile_form,
		'edit_password_form': edit_password_form
	})


@login_required
def logout_(request):
	logout(request)
	return redirect(request.GET.get('next', reverse('forum:index')))


@require_GET
def user(request, user_id):
	if user_id == request.user.id:
		return redirect('forum:profile')
	return render_with_tags(request, 'user.html', {
		'user': get_object_or_404(User, id=user_id)
	})


@require_GET
def users(request):  # TODO: переделать пагинацию
	paginator = Paginator(User.objects.all(), 10)
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
			question_ = form.save(commit=False)
			question_.author = request.user
			question_.save()
			question_.tags.set(form.cleaned_data['tags'])  # TODO: check why tags не запоминаются
			question_.save()
			return redirect('forum:question', question_id=question_.id)
	else:
		form = AskQuestionForm()
	return render_with_tags(request, 'ask.html', {
		'form': form
	})


def question(request, question_id):
	if request.user.is_authenticated and request.method == 'POST':
		answer_form = AnswerTheQuestionForm(request.POST)
		if answer_form.is_valid():
			answer = answer_form.save(commit=False)
			answer.author = request.user
			answer.save()
			Question.objects.get(id=answer.question_id).new_answer_posted()
	else:
		answer_form = AnswerTheQuestionForm(initial={
			'question': question_id
		})
	return render_with_tags(request, 'question.html', {
		'question': get_object_or_404(Question, id=question_id),
		'question_rating_form': QuestionRatingForm(initial={
			'question': question_id
		}),
		'comment_to_question_form': CommentToQuestionForm(initial={
			'question': question_id
		}),
		'answer_form': answer_form,
		# 'comment_to_answer_form': CommentToAnswerForm()
	})


@login_required
@require_POST
def ajax_comment_to_question(request):
	form = CommentToQuestionForm(request.POST)
	if form.is_valid():
		comment_to_question = form.save(commit=False)
		comment_to_question.author = request.user
		comment_to_question.save()
		return JsonResponse({
			# 'profile_url': reverse('forum:user', request.user.id),
			'avatar_url': request.user.avatar.url,  # TODO
			'text': comment_to_question.text
		})
	return JsonResponse({
		'error': form.errors.as_text()
	}, status=400)


@login_required
@require_POST
def ajax_rate_question(request):
	form = QuestionRatingForm(request.POST)
	if form.is_valid():
		question_ = form.cleaned_data['question']
		was_rated = question_.was_rated(request.user)
		if was_rated:
			question_.rating_remove(request.user)
		else:
			question_.rating_add(request.user, form.cleaned_data['like'])
		return JsonResponse({})
	return JsonResponse({
		'error': form.errors.as_text()
	}, status=400)


@require_GET
def hot(request):
	return render_questions(request, 'hot.html', {
		'pagination': Question.objects.get_hot(hot_questions_min_rating)
	})


@require_GET
def tag(request, tag_name):
	return render_questions(request, 'tag.html', {
		'tag_name': tag_name,
		'pagination': Question.objects.get_by_tag(get_object_or_404(QuestionTag, name=tag_name))
	})
