# Generated by Django 3.2.12 on 2022-05-23 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_profileskill_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(upload_to='project_images'),
        ),
    ]
