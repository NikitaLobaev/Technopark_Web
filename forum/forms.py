from django import forms

from forum.models import Question, User


class AuthForm(forms.ModelForm):
	username = forms.CharField(max_length=30, label='Логин')
	
	class Meta:
		abstract = True


class SignupForm(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name']


class LoginForm(forms.ModelForm):
	username = forms.CharField(max_length=30, label='Логин')
	
	class Meta:
		model = User
		fields = ['username', 'password']


class AskQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['author', 'title', 'text', 'tags', ]
