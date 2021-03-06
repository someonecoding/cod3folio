# Generated by Django 3.2.12 on 2022-04-17 19:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profileskill_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileskill',
            name='level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], validators=[django.core.validators.MinValueValidator(limit_value=0, message='0 to 5'), django.core.validators.MaxValueValidator(limit_value=5, message='0 to 5')]),
        ),
    ]
