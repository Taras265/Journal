# Generated by Django 3.2.6 on 2021-08-12 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0031_auto_20210812_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['topic'], 'verbose_name': 'Тема', 'verbose_name_plural': 'Теми'},
        ),
    ]