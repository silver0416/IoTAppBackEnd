# Generated by Django 4.0.6 on 2022-09-07 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_chat_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='mode_key_data',
            name='fan_spin',
            field=models.BooleanField(default=False),
        ),
    ]
