# Generated by Django 3.2.12 on 2022-05-15 22:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=500, validators=[django.core.validators.MinLengthValidator(50, 'Description must contain at least 50 characters.')]),
        ),
    ]