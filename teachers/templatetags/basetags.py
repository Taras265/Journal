from django import template
from django.contrib.auth.models import Group
from teachers.models import Teacher
from students.models import SchoolJournal
import datetime

now = datetime.datetime.now()
register = template.Library()


@register.filter
def class_teacher(user):
    group = Group.objects.get(name='Вчитель')
    if group in user.groups.all():
        teacher = Teacher.objects.get(user_id=user.pk)
        if SchoolJournal.objects.filter(class_teacher=teacher):
            return True
    return False
