# Generated by Django 3.0.6 on 2020-05-12 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commenttoanswer',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='commenttoquestion',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user__username']},
        ),
        migrations.AlterModelOptions(
            name='questiontag',
            options={'ordering': ['name']},
        ),
    ]
