# Generated by Django 3.1.7 on 2021-02-24 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.CharField(max_length=1024, verbose_name='Description')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='MCQOptions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('option', models.CharField(max_length=200, verbose_name='Option')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Correct answer?')),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_title', models.CharField(max_length=1024, verbose_name='Question title')),
                ('type_of_question', models.CharField(choices=[('MC', 'MCQ'), ('FI', 'Fill in the blanks')], default='UD', max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz_app.category')),
            ],
            options={
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='StudentQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer_given', models.CharField(blank=True, max_length=200, null=True, verbose_name='Answer Given by the student')),
                ('is_correct', models.BooleanField(verbose_name='Correct?')),
                ('option_choosed', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='quiz_app.mcqoptions')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz_app.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Progress',
            },
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField(verbose_name='Start time')),
                ('marks', models.CharField(max_length=50, verbose_name='Marks')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz_app.category')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Progress',
            },
        ),
        migrations.AddField(
            model_name='mcqoptions',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz_app.question'),
        ),
        migrations.CreateModel(
            name='FillInTheBlank',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('correct_answer', models.CharField(max_length=200, verbose_name='Option')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='quiz_app.question')),
            ],
            options={
                'verbose_name_plural': 'Fill In The Blanks',
            },
        ),
    ]
