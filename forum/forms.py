from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.forms import TextInput, PasswordInput, ModelForm, SelectMultiple, Textarea, HiddenInput

from forum.models import Question, User, Answer, CommentToQuestion, QuestionLike


class AuthFormMeta:
	labels = {
		'username': 'Логин',
		'password': 'Пароль',
		'email': 'Email',
		'first_name': 'Имя',
		'last_name': 'Фамилия',
		'avatar': 'Аватар'
	}
	model = User
	widgets = {
		'username': TextInput(attrs={
			'class': 'form-control'
		}),
		'password': PasswordInput(attrs={
			'class': 'form-control'
		}),
		'email': TextInput(attrs={
			'class': 'form-control'
		}),
		'first_name': TextInput(attrs={
			'class': 'form-control'
		}),
		'last_name': TextInput(attrs={
			'class': 'form-control'
		})
	}


class SignupForm(UserCreationForm):
	class Meta(AuthFormMeta):
		fields = ['username', 'email', 'first_name', 'last_name', 'avatar']


class LoginForm(AuthenticationForm):
	class Meta(AuthFormMeta):
		fields = ['username', 'password']


class EditProfileForm(ModelForm):
	class Meta(AuthFormMeta):
		fields = ['avatar', 'username', 'email', 'first_name', 'last_name']


class EditPasswordForm(PasswordChangeForm):  # TODO: не изменяется widget и атрибут class!!!
	class Meta(AuthFormMeta):
		fields = '__all__'


class AskQuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']
		labels = {
			'title': 'Заголовок',
			'text': 'Тело',
			'tags': 'Теги'
		}
		widgets = {
			'title': TextInput(attrs={
				'class': 'form-control'
			}),
			'text': TextInput(attrs={
				'class': 'form-control'
			}),
			'tags': SelectMultiple(attrs={
				'class': 'form-control'
			})
		}


class QuestionRatingForm(ModelForm):
	class Meta:
		fields = ['question', 'like']
		model = QuestionLike


class AnswerTheQuestionForm(ModelForm):
	class Meta:
		model = Answer
		fields = ['question', 'text']
		labels = {
			'text': 'Ответ'
		}
		widgets = {
			'question': HiddenInput(),
			'text': Textarea(attrs={
				'class': 'form-control',
				'rows': '6'
			})
		}


class CommentToQuestionForm(ModelForm):
	class Meta:
		model = CommentToQuestion
		fields = ['question', 'text']
		labels = {
			'text': 'Ответ'
		}
		widgets = {
			'question': HiddenInput(),
			'text': Textarea(attrs={
				'class': 'form-control',
				'rows': '3'
			})
		}


class PaginationForm(forms.Form):
	order = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class': 'form-control',
			'onchange': 'this.form.submit()'
		}), choices=[
			('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
			('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)'), ('title', 'заголовку')],
		initial='-pub_date', label='Сортировать по', required=False)
	limit = forms.ChoiceField(
		widget=forms.Select(attrs={
			'class': 'form-control',
			'onchange': 'this.form.submit()'
		}), choices=[('3', '3'), ('10', '10'), ('20', '20')], initial='3', label='Кол-во на страницу', required=True)
	page = forms.IntegerField(widget=forms.NumberInput(attrs={
		'class': 'form-control',
		'onchange': 'this.form.submit()'
	}), initial=1, label='Номер страницы', min_value=1, required=False)
	
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
