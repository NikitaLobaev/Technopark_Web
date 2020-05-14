from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from forum.models import User, QuestionTag, Question, QuestionLike, CommentToQuestion, Answer, AnswerLike, \
	CommentToAnswer

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(QuestionTag)
admin.site.register(Question)
admin.site.register(QuestionLike)
admin.site.register(CommentToQuestion)
admin.site.register(Answer)
admin.site.register(AnswerLike)
admin.site.register(CommentToAnswer)
