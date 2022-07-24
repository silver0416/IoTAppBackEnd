# Generated by Django 4.0.6 on 2022-07-24 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_alter_user_info_user_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='user_email',
            field=models.EmailField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='user_name',
            field=models.CharField(default=' ', max_length=30, unique=True),
        ),
    ]
