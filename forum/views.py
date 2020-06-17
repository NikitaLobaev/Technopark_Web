from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import RedirectView
from django.core.cache import cache

from forum.forms import SignupForm, LoginForm, EditProfileForm, EditPasswordForm, UsersPaginationForm, \
    AskQuestionForm, QuestionsPaginationForm, AnswerTheQuestionForm, QuestionRatingForm, CommentToQuestionForm
from forum.models import User, Question, QuestionTag, Answer


class BaseView(View):  # TODO: sort all imports!!!
    template_name = 'index.html'
    
    def get(self, request, **kwargs):
        kwargs['top_tags'] = cache.get('top_tags')
        kwargs['top_users'] = cache.get('top_users')
        return render(request, self.template_name, kwargs)


class PaginationView(BaseView):
    template_name = 'index.html'
    
    def get(self, request, **kwargs):
        pagination = kwargs.get('pagination', Question.objects.all())
        pagination_form = kwargs.get('pagination_form', QuestionsPaginationForm(request.GET or None))
        if pagination_form.is_valid():
            pagination = Paginator(pagination.order_by(pagination_form.cleaned_data['order']),
                                   pagination_form.cleaned_data['limit'])
            page = pagination_form.cleaned_data['page']
        else:
            pagination = Paginator(pagination, pagination_form.fields['limit'].initial)
            page = pagination_form.fields['page'].initial
        try:
            pagination = pagination.page(page)
        except PageNotAnInteger:
            return HttpResponseNotFound()
        except EmptyPage:
            pagination = pagination.page(pagination.num_pages)
        kwargs['pagination'] = pagination
        kwargs['pagination_form'] = pagination_form
        return super().get(request, **kwargs)


class SignupView(BaseView):
    template_name = 'signup.html'
    
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('forum:index')
        kwargs['form'] = SignupForm()
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('forum:index')
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                user = form.save()
                login(request, user)
                return redirect(request.GET.get('next', reverse('forum:index')))
        kwargs['form'] = form
        return super().get(request, **kwargs)


class LoginView(BaseView):
    template_name = 'login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('forum:index')
        kwargs['form'] = LoginForm()
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return redirect('forum:index')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', reverse('forum:index')))
        kwargs['form'] = form
        return super().get(request, **kwargs)


class UserView(BaseView):
    template_name = 'user.html'
    
    def get(self, request, **kwargs):
        if request.user.id == kwargs['id']:
            self.template_name = 'profile.html'
            kwargs['edit_profile_form'] = EditProfileForm(instance=request.user)
            kwargs['edit_password_form'] = EditPasswordForm(user=request.user)
        else:
            kwargs['user'] = get_object_or_404(User, id=kwargs['id'])
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        if not request.user.id == kwargs['id']:
            return HttpResponseForbidden()
        edit_profile_form = EditProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        edit_password_form = EditPasswordForm(data=request.POST, user=request.user)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
        elif edit_password_form.is_valid():
            edit_password_form.save()
        kwargs['edit_profile_form'] = edit_profile_form
        kwargs['edit_password_form'] = edit_password_form
        return super().get(request, **kwargs)


class LogoutView(RedirectView):
    url = reverse_lazy('forum:index')
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class UsersView(PaginationView):
    template_name = 'users.html'
    
    def get(self, request, **kwargs):
        kwargs['pagination'] = User.objects.all()
        kwargs['pagination_form'] = UsersPaginationForm(request.GET or None)
        return super().get(request, **kwargs)


class AskQuestionView(BaseView):
    template_name = 'ask.html'
    
    def get(self, request, **kwargs):
        kwargs['form'] = AskQuestionForm()
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        form = AskQuestionForm(data=request.POST, instance=Question(author=request.user))
        if form.is_valid():
            question = form.save()
            return redirect('forum:question', question_id=question.id)
        kwargs['form'] = form
        return super().get(request, **kwargs)


class QuestionView(PaginationView):
    template_name = 'question.html'
    
    def get(self, request, **kwargs):
        id_ = kwargs['id']
        question = get_object_or_404(Question, id=id_)
        kwargs['answer_form'] = AnswerTheQuestionForm(initial={
            'question': id_
        })
        kwargs['comment_to_question_form'] = CommentToQuestionForm()
        kwargs['pagination'] = question.get_answers()
        kwargs['question'] = question
        kwargs['question_rating_form'] = QuestionRatingForm(initial={
            'question': id_
        })
        return super().get(request, **kwargs)
    
    def post(self, request, **kwargs):
        id_ = kwargs['id']
        question = get_object_or_404(Question, id=id_)
        if not request.user.is_authenticated:
            response = redirect('forum:login')
            response['Location'] += '?next=' + reverse('forum:question', id_)
            return response
        answer_form = AnswerTheQuestionForm(data=request.POST, instance=Answer(author=request.user, question_id=id_))
        if answer_form.is_valid():
            answer = answer_form.save()
            answer.author.answer_added(question)
        kwargs['answer_form'] = answer_form
        kwargs['comment_to_question_form'] = CommentToQuestionForm()
        kwargs['pagination'] = question.get_answers()
        kwargs['question_rating_form'] = QuestionRatingForm(initial={
            'question': id_
        })
        return super().get(request, **kwargs)


class TopQuestionsView(PaginationView):
    template_name = 'top.html'
    
    def get(self, request, **kwargs):
        kwargs['pagination'] = cache.get('top_questions')
        return super().get(request, **kwargs)


class TagQuestionsView(PaginationView):
    template_name = 'tag.html'
    
    def get(self, request, **kwargs):
        kwargs['pagination'] = Question.objects.get_by_tag(get_object_or_404(QuestionTag, name=kwargs['name']))
        return super().get(request, **kwargs)
