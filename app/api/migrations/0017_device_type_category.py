# Generated by Django 4.0.6 on 2022-07-24 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_device_type_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_type',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.category_detail'),
            preserve_default=False,
        ),
    ]
