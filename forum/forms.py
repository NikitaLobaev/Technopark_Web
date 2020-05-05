from django import forms


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if ' ' in username:
			self.add_error('username', 'No whitespaces allowed in username!')
		return username
