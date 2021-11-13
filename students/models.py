from django.contrib.auth.models import User
from django.db import models


class SchoolJournal(models.Model):
    class_num = models.PositiveSmallIntegerField(unique=False,
                                                 verbose_name='Номер класса')
    class_letter = models.CharField(max_length=1, unique=False,
                                    verbose_name='Буква класса')
    year = models.DateField(max_length=50, unique=False,
                            verbose_name="Навчальний рік")
    class_teacher = models.OneToOneField("teachers.Teacher", on_delete=models.CASCADE, verbose_name='Teacher ID')

    def __str__(self):
        return str(self.class_num) + '-' + self.class_letter.upper()

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журнали'


class Student(models.Model):
    name = models.CharField(max_length=50, unique=False,
                            verbose_name="Iм'я")
    so_name = models.CharField(max_length=50, unique=False,
                               verbose_name="Прізвище")
    second_name = models.CharField(max_length=50, unique=False,
                                   verbose_name="По батькові")
    date = models.DateField(max_length=50, unique=False,
                            verbose_name="Дата народження")
    address = models.TextField(max_length=50, unique=False,
                               verbose_name="Адреса")
    user_id = models.OneToOneField(User, unique=True, on_delete=models.CASCADE,
                                   related_name='user_id_set', verbose_name='Індефікатор')
    journal_id = models.ForeignKey(SchoolJournal, unique=False, on_delete=models.CASCADE,
                                   related_name='journal_id_set', verbose_name='Журнал')

    def __str__(self):
        return self.so_name + ' ' + self.name

    class Meta:
        verbose_name = 'Учень'
        verbose_name_plural = 'Учні'
        ordering = ['so_name']


class ClassSubjects(models.Model):
    class_num = models.PositiveSmallIntegerField(unique=True, verbose_name='Номер классу')
    subjects = models.ManyToManyField("teachers.Subject", verbose_name='Предмети')

    def __str__(self):
        return str(self.class_num)

    class Meta:
        verbose_name = 'Предмети класу'
        verbose_name_plural = 'Предмети класу'
        ordering = ['class_num']
