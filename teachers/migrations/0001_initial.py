# Generated by Django 3.2.5 on 2021-07-18 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предмети',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name="Iм'я")),
                ('so_name', models.CharField(max_length=50, unique=True, verbose_name='Прізвище')),
                ('second_name', models.CharField(max_length=50, unique=True, verbose_name='По батькові')),
                ('data', models.DateField(max_length=50, unique=True, verbose_name='Дата народження')),
                ('address', models.TextField(max_length=50, unique=True, verbose_name='Адреса')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_id_set', to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Вчитель',
                'verbose_name_plural': 'Вчителi',
                'ordering': ['so_name'],
            },
        ),
        migrations.CreateModel(
            name='TeacherSubjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.ManyToManyField(to='teachers.Subject', verbose_name='Сиписок предметiв')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_id_set', to='teachers.teacher', verbose_name='Teacher ID')),
            ],
            options={
                'verbose_name': 'Сиписок предметiв',
                'verbose_name_plural': 'Сиписок предметiв',
            },
        ),
    ]
