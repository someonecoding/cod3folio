# Generated by Django 3.2.12 on 2022-05-15 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_profileskill_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='position',
            field=models.CharField(default='Developer', max_length=100),
        ),
    ]
