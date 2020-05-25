# Generated by Django 3.0.6 on 2020-05-17 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20200514_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerlike',
            name='question',
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='/static/default_avatar.png', upload_to='avatar'),
        ),
    ]