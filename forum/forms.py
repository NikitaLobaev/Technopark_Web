from django import forms

from forum.models import Question


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if ' ' in username:
			self.add_error('username', 'No whitespaces allowed in username!')
		return username


class AskQuestionForm(forms.Form):
	title = forms.CharField(max_length=256)
	text = forms.CharField(widget=forms.Textarea)
	# tags = forms.ManyToManyField(QuestionTag)
	
	def __init__(self, author, **kwargs):
		self._author = author
		super(AskQuestionForm, self).__init__(**kwargs)
	
	def clean(self):
		pass
	
	def save(self):
		self.cleaned_data['author'] = self._author
		return Question.manager.create(**self.cleaned_data)
