# Generated by Django 3.2.5 on 2021-08-05 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0024_alter_topic_class_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='class_teacher',
        ),
    ]