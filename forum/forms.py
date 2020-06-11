from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)

from forum.models import (Answer, CommentToQuestion, Question, QuestionLike,
                          User)


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = self.fields['first_name'].widget.attrs = \
            self.fields['last_name'].widget.attrs = self.fields['username'].widget.attrs = \
            self.fields['password1'].widget.attrs = self.fields['password2'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['avatar'].widget.attrs = {
            'class': 'form-control-file'
        }
    
    class Meta:
        fields = ['avatar', 'email', 'username', 'first_name', 'last_name']
        labels = {
            'avatar': 'Аватар',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Логин'
        }
        model = User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs = self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }
    
    class Meta:
        fields = ['username', 'password']
        labels = {
            'password': 'Пароль',
            'username': 'Логин'
        }
        model = User


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = self.fields['first_name'].widget.attrs = \
            self.fields['last_name'].widget.attrs = self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['avatar'].widget.attrs = {
            'class': 'form-control-file'
        }
    
    class Meta(SignupForm.Meta):
        pass


class EditPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = self.fields['new_password1'].widget.attrs = \
            self.fields['new_password2'].widget.attrs = {
            'class': 'form-control'
        }


class AskQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = self.fields['text'].widget.attrs = \
            self.fields['tags'].widget.attrs = {
            'class': 'form-control'
        }
    
    class Meta:
        fields = ['title', 'text', 'tags']
        labels = {
            'tags': 'Теги',
            'text': 'Тело',
            'title': 'Заголовок',
        }
        model = Question


class QuestionRatingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs = {  # TODO: возможно, не нужно здесь поле question...
            'class': 'form-control',
            'rows': '6'
        }
    
    class Meta:
        fields = ['like', 'question']
        model = QuestionLike


class AnswerTheQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {
            'class': 'form-control',
            'rows': '6'
        }
    
    class Meta:
        fields = ['text']
        labels = {
            'text': 'Ответ'
        }
        model = Answer


class CommentToQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs = {
            'class': 'form-control',
            'rows': '3'
        }
    
    class Meta:
        fields = ['text']
        labels = {
            'text': 'Ответ'
        }
        model = CommentToQuestion


class QuestionsPaginationForm(forms.Form):
    order = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
        'onchange': 'this.form.submit()'
    }), choices=[('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
                 ('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)'),
                 ('-title', 'заголовку (по убыванию)'), ('title', 'заголовку (по возрастанию)')],
        initial='-pub_date', label='Сортировать по', required=False)
    limit = forms.ChoiceField(widget=forms.Select(attrs={
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
            return self.fields['order'].initial
    
    def clean_limit(self):
        limit = self.cleaned_data['limit']
        if limit:
            return limit
        else:
            return self.fields['limit'].initial
    
    def clean_page(self):
        page = self.cleaned_data['page']
        if page:
            return page
        else:
            return self.fields['page'].initial


class AnswersPaginationForm(QuestionsPaginationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].choices = [('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
                                        ('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)')]


class UsersPaginationForm(QuestionsPaginationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order'].choices = [('-answers_count', 'популярности (по кол-ву ответов)'),
                                        ('username', 'имени (по возрастанию)'), ('-username', 'имени (по убыванию)')]
        self.fields['order'].initial = '-answers_count'
        self.fields['limit'].choices = [('10', '10'), ('30', '30'), ('50', '50')]
        self.fields['limit'].initial = '30'
