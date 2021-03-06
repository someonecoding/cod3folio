# Generated by Django 3.2.12 on 2022-04-13 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../static/img/defaultuser.jpg', upload_to='avatars'),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='surname',
            field=models.CharField(default='', max_length=100),
        ),
    ]
