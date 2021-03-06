# Generated by Django 3.2.5 on 2021-07-21 16:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0002_alter_schooljournal_class_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name="Iм'я")),
                ('so_name', models.CharField(max_length=50, verbose_name='Прізвище')),
                ('second_name', models.CharField(max_length=50, verbose_name='По батькові')),
                ('date', models.DateField(max_length=50, verbose_name='Дата народження')),
                ('address', models.TextField(max_length=50, verbose_name='Адреса')),
                ('journal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_id_set', to='students.schooljournal', verbose_name='Журнал')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_id_set', to=settings.AUTH_USER_MODEL, verbose_name='Індефікатор')),
            ],
            options={
                'verbose_name': 'Вчитель',
                'verbose_name_plural': 'Вчителi',
                'ordering': ['so_name'],
            },
        ),
    ]
