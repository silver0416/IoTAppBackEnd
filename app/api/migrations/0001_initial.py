# Generated by Django 4.1 on 2022-09-07 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=30, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("password", models.TextField(default=" ")),
                (
                    "user_nickname",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                ("user_phone", models.CharField(blank=True, max_length=30, null=True)),
                ("email", models.EmailField(max_length=30, null=True, unique=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "使用者",
                "verbose_name_plural": "使用者",
            },
        ),
        migrations.CreateModel(
            name="chat_room_data",
            fields=[
                (
                    "message_id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("chat_room_name", models.CharField(max_length=30)),
                ("message", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="home_list",
            fields=[
                (
                    "home_id",
                    hashid_field.field.HashidAutoField(
                        alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
                        min_length=8,
                        prefix="",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("home_name", models.CharField(max_length=30)),
                (
                    "user",
                    models.ManyToManyField(
                        related_name="detail", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "家庭",
                "verbose_name_plural": "家庭",
            },
        ),
        migrations.CreateModel(
            name="mode_key_data",
            fields=[
                (
                    "mode_key_data_id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("mode_key_name", models.CharField(default=False, max_length=30)),
                ("tplink_switch_mode_key", models.CharField(max_length=6)),
                ("ac_temperature", models.SmallIntegerField(default=25)),
                ("ac_switch", models.BooleanField(default=False)),
                ("fan_level", models.SmallIntegerField(default=1)),
                ("fan_switch", models.BooleanField(default=False)),
                ("mode_key_time", models.DateTimeField(auto_now_add=True)),
                (
                    "home_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.home_list"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="home_admin",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                (
                    "admin",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "home",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="api.home_list"
                    ),
                ),
            ],
            options={
                "verbose_name": "家庭管理員",
                "verbose_name_plural": "家庭管理員",
            },
        ),
        migrations.CreateModel(
            name="device_list",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("added_time", models.DateTimeField(auto_now=True)),
                ("type_name", models.CharField(max_length=30)),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.home_list"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="device_data",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("data", models.JSONField()),
                ("data_time", models.DateTimeField(auto_now_add=True)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.device_list",
                    ),
                ),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.home_list"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="chat_room",
            fields=[
                (
                    "chat_room_name",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                (
                    "message",
                    models.ManyToManyField(
                        related_name="chat_room_message", to="api.chat_room_data"
                    ),
                ),
            ],
        ),
    ]
