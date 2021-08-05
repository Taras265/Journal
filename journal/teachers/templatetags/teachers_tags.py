from django import template
from django.contrib.auth.models import Group
from teachers.models import Mark, MarkType
import datetime

now = datetime.datetime.now()
register = template.Library()


@register.filter
def teacher(user):
    group = Group.objects.get(name='Вчитель')
    return True if group in user.groups.all() else False


@register.filter
def mark_filter(date, student):
    marks = Mark.objects.filter(student=student.id, date=date)
    if marks:
        return True
    return False


@register.filter
def get_simple_mark(date, student):
    simple_mark = MarkType.objects.get(pk=2)
    mark = Mark.objects.get(student=student.id, date=date, type=simple_mark)
    return mark


@register.filter
def form(data):
    return True if data else False


@register.filter
def date_filter(dates):
    if dates:
        return True if now.date() > max(dates) else False
    return True


@register.filter
def date_today(t):
    return str(now.date())
