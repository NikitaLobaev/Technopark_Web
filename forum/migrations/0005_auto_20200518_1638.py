# Generated by Django 3.0.6 on 2020-05-18 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20200517_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='default_avatar.png', upload_to=''),
        ),
    ]
