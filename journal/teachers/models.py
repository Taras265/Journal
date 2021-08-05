from django.contrib.auth.models import User
from django.db import models
from students.models import SchoolJournal, Student


class Teacher(models.Model):
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
    user_id = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, verbose_name='Індефікатор')

    def __str__(self):
        return self.name + ' ' + self.so_name + ' ' + self.second_name

    class Meta:
        verbose_name = 'Вчитель'
        verbose_name_plural = 'Вчителi'
        ordering = ['so_name']


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Предмет')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предмети'
        ordering = ['name']


class TeacherSubjects(models.Model):
    subjects = models.ManyToManyField(Subject, verbose_name='Сиписок предметiв')
    teacher_id = models.OneToOneField(Teacher, on_delete=models.CASCADE, verbose_name='Teacher ID')

    def __str__(self):
        u = Teacher.objects.get(pk=self.teacher_id.id)
        return u.name + ' ' + u.so_name + ' ' + u.second_name

    class Meta:
        verbose_name = 'Сиписок предметiв'
        verbose_name_plural = 'Сиписок предметiв'


class ClassTeacher(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                   related_name='class_teacher_subject', verbose_name='Предмет')
    journal_id = models.ForeignKey(SchoolJournal, on_delete=models.CASCADE,
                                   related_name='class_teacher_journal', verbose_name='Журнал')
    teacher_id = models.ForeignKey(TeacherSubjects, on_delete=models.CASCADE,
                                   related_name='class_teacher', verbose_name='Вчитель')

    def __str__(self):
        return self.teacher_id.teacher_id.name + ' ' + \
               self.teacher_id.teacher_id.so_name + ' ' + \
               self.teacher_id.teacher_id.second_name + \
               ' - вчитель ' \
               + str(self.journal_id.class_num) + '-' + self.journal_id.class_letter.upper()

    class Meta:
        verbose_name = 'Предмет вчителя'
        verbose_name_plural = 'Предмети вчителів'
        ordering = ['journal_id']


class MarkType(models.Model):
    type = models.CharField(max_length=20, unique=True, verbose_name='Тип оцінки')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип оцінки'
        verbose_name_plural = 'Типи оцінки'
        ordering = ['type']


class Topic(models.Model):
    topic = models.TextField(max_length=50, unique=False, verbose_name='Тема')
    start = models.DateField(unique=False, verbose_name='Дата початку')
    finish = models.DateField(unique=False, blank=True, null=True, verbose_name='Дата закінченя')
    class_teacher = models.ForeignKey(ClassTeacher, null=True, on_delete=models.CASCADE,
                                      related_name='class_teacher_choice', verbose_name="Вчитель")

    def __str__(self):
        return str(self.topic)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Теми'
        ordering = ['topic']


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_mark_id',
                                verbose_name='Учень')
    date = models.DateField(unique=False, verbose_name='Дата')
    mark = models.SmallIntegerField(unique=False, verbose_name='Оцінка')
    teacher = models.ForeignKey(ClassTeacher, on_delete=models.CASCADE,
                                related_name='teacher_mark_id', verbose_name='Вчитель')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_mark_id',
                                verbose_name='Предмет')
    type = models.ForeignKey(MarkType, on_delete=models.CASCADE, related_name='type_id',
                             verbose_name='Тип')
    topic = models.ForeignKey(Topic, blank=True, null=True, on_delete=models.CASCADE,
                              related_name='type_id',
                              verbose_name='Тема')

    def __str__(self):
        return str(self.mark)

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        ordering = ['type']
