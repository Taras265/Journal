# Generated by Django 3.2.5 on 2021-07-20 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0005_alter_teacher_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user_id'),
        ),
    ]
