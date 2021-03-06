# Generated by Django 3.2.5 on 2021-07-28 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20210722_1259'),
        ('teachers', '0019_auto_20210728_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('mark', models.SmallIntegerField(verbose_name='Оцінка')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mark_id', to='students.student', verbose_name='Вчитель')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_mark_id', to='teachers.subject', verbose_name='Предмет')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_mark_id', to='teachers.teachersubjects', verbose_name='Вчитель')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_id', to='teachers.marktype', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Тип оцінки',
                'verbose_name_plural': 'Типи оцінки',
                'ordering': ['type'],
            },
        ),
    ]
