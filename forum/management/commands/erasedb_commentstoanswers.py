from django.core.management.base import BaseCommand

from forum.models import CommentToAnswer


class Command(BaseCommand):
    help = 'Очистка БД: комментарии к ответам'
    
    def handle(self, *args, **options):
        CommentToAnswer.objects.all().delete()
        print('erasedb_commentstoanswer: OK')
