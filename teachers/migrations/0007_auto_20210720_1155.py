# Generated by Django 3.2.5 on 2021-07-20 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0006_alter_teacher_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='address',
            field=models.TextField(max_length=50, verbose_name='Адреса'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='date1',
            field=models.DateField(max_length=50, verbose_name='Дата народження'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=50, verbose_name="Iм'я"),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='second_name',
            field=models.CharField(max_length=50, verbose_name='По батькові'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='so_name',
            field=models.CharField(max_length=50, verbose_name='Прізвище'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='user_id'),
        ),
    ]
