from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.PaginationView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', login_required(views.LogoutView.as_view()), name='logout'),
    path('user/<int:id>/', login_required(views.UserView.as_view()), name='user'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('ask/', login_required(views.AskQuestionView.as_view()), name='ask'),
    path('question/<int:id>/', views.QuestionView.as_view(), name='question'),
    path('top/', views.TopQuestionsView.as_view(), name='top'),
    path('tag/<str:name>/', views.TagQuestionsView.as_view(), name='tag')
]
