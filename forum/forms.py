from django import forms

from forum.models import Question, User


class AuthForm(forms.ModelForm):
	class Meta:
		abstract = True
		model = User
		fields = []
		labels = {
			'username': 'Логин',
			'password': 'Пароль',
			'email': 'Email',
			'first_name': 'Имя',
			'last_name': 'Фамилия',
			'avatar': 'Аватар'
		}


class SignupForm(AuthForm):
	class Meta(AuthForm.Meta):
		abstract = False
		fields = ['username', 'password', 'email', 'first_name', 'last_name']


class LoginForm(AuthForm):
	class Meta(AuthForm.Meta):
		abstract = False
		fields = ['username', 'password']


class EditPasswordForm(AuthForm):
	password_old = User.password
	password_repeat = User.password
	
	class Meta(AuthForm.Meta):
		abstract = False
		fields = ['password']
		labels = {
			'password_old': 'Старый пароль',
			'password': 'Новый пароль',
			'password_repeat': 'Повторите новый пароль'
		}


class EditAvatarForm(AuthForm):
	class Meta(AuthForm.Meta):
		abstract = False
		fields = ['avatar']


class AskQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'text', 'tags']
		labels = {
			'title': 'Заголовок',
			'text': 'Тело',
			'tags': 'Теги'
		}


class QuestionsPaginationForm(forms.Form):
	order = forms.ChoiceField(
		widget=forms.Select(attrs={
			'onchange': 'this.form.submit()'
		}), choices=[
			('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
			('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)'), ('title', 'заголовку')],
		label='Сортировать по', required=False)
	limit = forms.ChoiceField(
		widget=forms.Select(attrs={
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
