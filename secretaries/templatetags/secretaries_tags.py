from django import template
from django.contrib.auth.models import Group
from teachers.models import ClassTeacher, SchoolJournal
from students.models import ClassSubjects

register = template.Library()


@register.filter('secretary')
def secretary(user):
    group = Group.objects.get(name='Секретар')
    return True if group in user.groups.all() else False


@register.filter
def get_teacher(subject, journal):
    teachers_class = ClassTeacher.objects.filter(journal_id=journal, subject_id=subject)
    if teachers_class:
        return teachers_class[0].teacher_id
    return "Нема"


@register.filter
def get_teacher_id(subject, journal):
    id = ClassTeacher.objects.filter(journal_id=journal, subject_id=subject)[0].id
    return id


@register.filter
def teacher_filter(subject, journal):
    teachers_class = ClassTeacher.objects.filter(journal_id=journal, subject_id=subject)
    if teachers_class:
        return True
    return False


@register.filter
def class_subject(journal):
    return ClassSubjects.objects.filter(class_num=journal.journal_id.class_num)[0].subjects.all()
