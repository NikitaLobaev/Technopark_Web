from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, UserCreationForm)
from django.forms import (HiddenInput, ModelForm, PasswordInput, SelectMultiple, Textarea, TextInput, Form, ChoiceField,
                          Select, IntegerField, NumberInput)

from forum.models import (Answer, CommentToQuestion, Question, QuestionLike, User)


class AuthFormMeta:
    labels = {
        'avatar': 'Аватар',
        'email': 'Email',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'password': 'Пароль',
        'username': 'Логин'
    }
    model = User
    widgets = {
        'email': TextInput(attrs={
            'class': 'form-control'
        }),
        'first_name': TextInput(attrs={
            'class': 'form-control'
        }),
        'last_name': TextInput(attrs={
            'class': 'form-control'
        }),
        'password': PasswordInput(attrs={
            'class': 'form-control'
        }),
        'password1': PasswordInput(attrs={
            'class': 'form-control'
        }),
        'password2': PasswordInput(attrs={
            'class': 'form-control'
        }),
        'username': TextInput(attrs={
            'class': 'form-control'
        })
    }


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = self.fields['password2'].widget.attrs = {  # TODO: плохо задаются стили
            'class': 'form-control'
        }
        self.fields['avatar'].widget.attrs = {
            'class': 'form-control-file'
        }
    
    class Meta(AuthFormMeta):
        fields = ['avatar', 'email', 'first_name', 'last_name', 'username']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['username'].widget.attrs = self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }
    
    class Meta(AuthFormMeta):
        fields = ['password', 'username']


class EditProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].widget.attrs = {
            'class': 'form-control-file'
        }
    
    class Meta(AuthFormMeta):
        fields = ['avatar', 'username', 'email', 'first_name', 'last_name']


class EditPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = self.fields['new_password1'].widget.attrs = \
            self.fields['new_password2'].widget.attrs = {
            'class': 'form-control'
        }
    
    class Meta(AuthFormMeta):
        fields = '__all__'


class AskQuestionForm(ModelForm):
    class Meta:
        fields = ['tags', 'text', 'title']
        labels = {
            'tags': 'Теги',
            'text': 'Тело',
            'title': 'Заголовок',
        }
        model = Question
        widgets = {
            'tags': SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'text': TextInput(attrs={
                'class': 'form-control'
            }),
            'title': TextInput(attrs={
                'class': 'form-control'
            })
        }


class QuestionRatingForm(ModelForm):
    class Meta:
        fields = ['question', 'like']
        model = QuestionLike


class AnswerTheQuestionForm(ModelForm):
    class Meta:
        fields = ['text']
        labels = {
            'text': 'Ответ'
        }
        model = Answer
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': '6'
            })
        }


class CommentToQuestionForm(ModelForm):
    class Meta:
        fields = ['question', 'text']
        labels = {
            'text': 'Ответ'
        }
        model = CommentToQuestion
        widgets = {
            'question': HiddenInput(),
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': '3'
            })
        }


class QuestionsPaginationForm(Form):
    order = ChoiceField(widget=Select(attrs={
        'class': 'form-control',
        'onchange': 'this.form.submit()'
    }), choices=[('-pub_date', 'дате (по убыванию)'), ('pub_date', 'дате (по возрастанию)'),
                 ('-rating', 'рейтингу (по убыванию)'), ('rating', 'рейтингу (по возрастанию)'),
                 ('-title', 'заголовку (по убыванию)'), ('title', 'заголовку (по возрастанию)')],
        initial='-pub_date', label='Сортировать по', required=False)
    limit = ChoiceField(widget=Select(attrs={
        'class': 'form-control',
        'onchange': 'this.form.submit()'
    }), choices=[('3', '3'), ('10', '10'), ('20', '20')], initial='3', label='Кол-во на страницу', required=True)
    page = IntegerField(widget=NumberInput(attrs={
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
