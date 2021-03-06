# Generated by Django 3.2.5 on 2021-07-23 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20210722_1259'),
        ('teachers', '0015_alter_classteacher_journal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classteacher',
            name='journal_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher_journal', to='students.schooljournal', verbose_name='Журнал'),
        ),
        migrations.AlterField(
            model_name='classteacher',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher_subject', to='teachers.subject', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='classteacher',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher', to='teachers.teacher', verbose_name='Вчитель'),
        ),
    ]
