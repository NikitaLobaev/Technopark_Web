from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_, name='login'),
	path('profile/', views.profile, name='profile'),
	# path('profile/edit/avatar/', views.profile_edit_avatar, name='profile_edit_avatar'),
	# path('profile/edit/password/', views.profile_edit_password, name='profile_edit_password'),
	path('logout/', views.logout_, name='logout'),
	path('user/<int:user_id>/', views.user, name='user'),
	path('users/', views.users, name='users'),
	path('ask/', views.ask, name='ask'),
	path('question/<int:question_id>/', views.question, name='question'),
	path('hot/', views.hot, name='hot'),
	path('tag/<str:tag_name>/', views.tag, name='tag')
]
