# Generated by Django 3.2.5 on 2021-07-21 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0011_alter_teachersubjects_teacher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachersubjects',
            name='teacher_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher', verbose_name='Teacher ID'),
        ),
    ]
