from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('login/', views.login_, name='login'),
	path('profile/', views.profile, name='profile'),
	path('logout/', views.logout_, name='logout'),
	path('user/<int:user_id>/', views.user, name='user'),
	path('users/', views.users, name='users'),
	path('ask/', views.ask, name='ask'),
	path('question/<int:question_id>/', views.question, name='question'),
	path('ajax/comment_to_question', views.ajax_comment_to_question, name='ajax_comment_to_question'),
	path('ajax/rate_question', views.ajax_rate_question, name='ajax_rate_question'),
	# path('answer/<int:answer_id>/comment/', views.answer_comment, name='answer.comment'),
	path('hot/', views.hot, name='hot'),
	path('tag/<str:tag_name>/', views.tag, name='tag')
]
