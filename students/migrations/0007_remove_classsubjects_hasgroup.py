# Generated by Django 3.2.6 on 2021-12-11 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_classsubjects_hasgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classsubjects',
            name='hasGroup',
        ),
    ]