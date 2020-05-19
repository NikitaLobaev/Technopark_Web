from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from forum.models import Question, User, Answer


class AuthFormMeta:
	model = User
	labels = {
		'username': 'Логин',
		'password': 'Пароль',
		'email': 'Email',
		'first_name': 'Имя',
		'last_name': 'Фамилия',
		'avatar': 'Аватар'
	}


class SignupForm(UserCreationForm):
	class Meta(AuthFormMeta):
		fields = ['username', 'email', 'first_name', 'last_name', 'avatar']


class LoginForm(AuthenticationForm):
	class Meta(AuthFormMeta):
		fields = ['username', 'password']


class EditProfileForm(forms.ModelForm):
	class Meta(AuthFormMeta):
		fields = ['avatar', 'username', 'email', 'first_name', 'last_name']


class EditPasswordForm(forms.ModelForm):
	password_old = forms.CharField(max_length=100)
	password_repeat = forms.CharField(max_length=100)
	
	class Meta(AuthFormMeta):
		fields = ['password_old', 'password', 'password_repeat']
		labels = {
			'password_old': 'Старый пароль',
			'password': 'Новый пароль',
			'password_repeat': 'Повторите новый пароль'
		}


class AskQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']
		labels = {
			'title': 'Заголовок',
			'text': 'Тело',
			'tags': 'Теги'
		}


class AnswerTheQuestionForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['text']
		labels = {
			'text': 'Ответ'
		}


class QuestionsPaginationForm(forms.Form):
	order = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class': 'form-control',
			'onchange': 'this.form.submit()'
		}), choices=[
			('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
			('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)'), ('title', 'заголовку')],
		label='Сортировать по', required=False)
	limit = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class': 'form-control',
			'onchange': 'this.form.submit()'
		}), choices=[('3', '3'), ('10', '10'), ('20', '20')], label='Вопросов на страницу', required=False)
	page = forms.IntegerField(widget=forms.HiddenInput(), min_value=1, required=False)
	
	def clean_order(self):
		order = self.cleaned_data['order']
		if order:
			return order
		else:
			return '-pub_date'
	
	def clean_limit(self):
		limit = self.cleaned_data['limit']
		if limit:
			return limit
		else:
			return '3'
	
	def clean_page(self):
		page = self.cleaned_data['page']
		if page:
			return page
		else:
			return 1
