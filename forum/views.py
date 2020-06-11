from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from forum.forms import (AnswersPaginationForm, AnswerTheQuestionForm,
                         AskQuestionForm, CommentToQuestionForm,
                         EditPasswordForm, EditProfileForm, LoginForm,
                         QuestionRatingForm, QuestionsPaginationForm,
                         SignupForm, UsersPaginationForm)
from forum.models import Answer, CommentToQuestion, Question, QuestionTag, User


def render_with_cache(request, template_name, context):
    context['top_tags'] = cache.get('top_tags')
    context['top_users'] = cache.get('top_users')
    return render(request, template_name, context)


def render_pagination(request, template_name, context, pagination_form):
    pagination = context['pagination']
    if pagination_form.is_valid():
        paginator = Paginator(pagination.order_by(pagination_form.cleaned_data['order']),
                              pagination_form.cleaned_data['limit'])
        page = pagination_form.cleaned_data['page']
    else:
        paginator = Paginator(pagination, pagination_form.fields['limit'].initial)
        page = pagination_form.fields['page'].initial
    try:
        context['pagination'] = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseNotFound()
    except EmptyPage:
        context['pagination'] = paginator.page(paginator.num_pages)
    context['pagination_form'] = pagination_form
    return render_with_cache(request, template_name, context)


@require_GET
def index(request):
    return render_pagination(request, 'index.html', {
        'pagination': Question.objects.all()
    }, QuestionsPaginationForm(request.GET or None))


def signup(request):
    if request.user.is_authenticated:
        return redirect('forum:index')
    if request.method == 'POST':
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                user_ = form.save()
                login(request, user_)
                return redirect(request.GET.get('next', reverse('forum:index')))
    else:
        form = SignupForm()
    return render_with_cache(request, 'signup.html', {
        'form': form
    })


def login_(request):
    if request.user.is_authenticated:
        return redirect('forum:index')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_ = authenticate(request, username=form.cleaned_data['username'],
                                 password=form.cleaned_data['password'])
            if user_:
                login(request, user_)
                return redirect(request.GET.get('next', reverse('forum:index')))
    else:
        form = LoginForm()
    return render_with_cache(request, 'login.html', {
        'form': form
    })


@login_required
def profile(request):
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        edit_password_form = EditPasswordForm(data=request.POST, user=request.user)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
        elif edit_password_form.is_valid():
            edit_password_form.save()
    else:
        edit_profile_form = EditProfileForm(instance=request.user)
        edit_password_form = EditPasswordForm(user=request.user)
    return render_with_cache(request, 'profile.html', {
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
    return render_with_cache(request, 'user.html', {
        'user': get_object_or_404(User, id=user_id)
    })


@require_GET
def users(request):
    return render_pagination(request, 'users.html', {
        'pagination_form': UsersPaginationForm,
        'pagination': User.objects.all()
    }, UsersPaginationForm(request.GET or None))


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskQuestionForm(data=request.POST, instance=Question(author=request.user))
        if form.is_valid():
            question_ = form.save()
            return redirect('forum:question', question_id=question_.id)
    else:
        form = AskQuestionForm()
    return render_with_cache(request, 'ask.html', {
        'form': form
    })


def question(request, question_id):
    question_ = get_object_or_404(Question, id=question_id)
    if request.user.is_authenticated and request.method == 'POST':
        answer_form = AnswerTheQuestionForm(request.POST, instance=Answer(author=request.user, question_id=question_id))
        if answer_form.is_valid():
            answer = answer_form.save()
            answer.author.answer_added(question_)
    else:
        answer_form = AnswerTheQuestionForm(initial={
            'question': question_id
        })
    return render_pagination(request, 'question.html', {
        'question': question_,
        'question_rating_form': QuestionRatingForm(initial={
            'question': question_id
        }),
        'comment_to_question_form': CommentToQuestionForm(),
        'answer_form': answer_form,
        'pagination': question_.get_answers()
    }, AnswersPaginationForm(request.GET or None))


@login_required
@require_POST
def ajax_comment_to_question(request):
    form = CommentToQuestionForm(data=request.POST, instance=CommentToQuestion(author=request.user))
    if form.is_valid():
        comment_to_question = form.save()
        return JsonResponse({
            'profile_url': reverse('forum:user', kwargs={
                'user_id': request.user.id
            }),
            'avatar_url': comment_to_question.author.avatar.url,
            'author': request.user.username,
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
def top(request):
    return render_pagination(request, 'top.html', {
        'pagination': cache.get('top_questions')
    }, QuestionsPaginationForm(request.GET or None))


@require_GET
def tag(request, tag_name):
    return render_pagination(request, 'tag.html', {
        'tag_name': tag_name,
        'pagination': Question.objects.get_by_tag(get_object_or_404(QuestionTag, name=tag_name))
    }, QuestionsPaginationForm(request.GET or None))
