# Generated by Django 4.1 on 2022-08-18 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_uid', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.TextField(default=' ')),
                ('user_nickname', models.CharField(blank=True, max_length=30, null=True)),
                ('user_phone', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=30, null=True, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '使用者',
                'verbose_name_plural': '使用者',
            },
        ),
        migrations.CreateModel(
            name='added_device_list',
            fields=[
                ('added_device_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('added_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='category_detail',
            fields=[
                ('category_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=30)),
                ('category_description', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='home_list',
            fields=[
                ('home_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('home_name', models.CharField(max_length=30)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '家庭',
                'verbose_name_plural': '家庭',
            },
        ),
        migrations.CreateModel(
            name='home_admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('home', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.home_list')),
            ],
            options={
                'verbose_name': '家庭管理員',
                'verbose_name_plural': '家庭管理員',
            },
        ),
        migrations.CreateModel(
            name='device_type',
            fields=[
                ('device_type_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('device_type_name', models.CharField(max_length=30)),
                ('device_type_description', models.CharField(blank=True, max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category_detail')),
            ],
        ),
        migrations.CreateModel(
            name='device_data',
            fields=[
                ('device_data_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('data_value', models.CharField(max_length=30)),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.added_device_list')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.device_type')),
            ],
        ),
        migrations.AddField(
            model_name='added_device_list',
            name='device_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.device_type'),
        ),
        migrations.AddField(
            model_name='added_device_list',
            name='home_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.home_list'),
        ),
    ]
