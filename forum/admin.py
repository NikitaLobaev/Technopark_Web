from django.contrib import admin

from forum.models import Profile, QuestionTag, Question, QuestionLikes, CommentToQuestion, Answer, AnswerLikes, \
	CommentToAnswer

admin.site.register(Profile)
admin.site.register(QuestionTag)
admin.site.register(Question)
admin.site.register(QuestionLikes)
admin.site.register(CommentToQuestion)
admin.site.register(Answer)
admin.site.register(AnswerLikes)
admin.site.register(CommentToAnswer)
