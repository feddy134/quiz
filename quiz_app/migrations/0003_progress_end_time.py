# Generated by Django 3.1.7 on 2021-03-03 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0002_auto_20210224_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='End time'),
            preserve_default=False,
        ),
    ]
