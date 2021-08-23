from django import template
from django.contrib.auth.models import Group
from teachers.models import Mark, MarkType, Topic
import datetime

now = datetime.datetime.now()
register = template.Library()


@register.filter
def teacher(user):
    group = Group.objects.get(name='Вчитель')
    return True if group in user.groups.all() else False


@register.filter
def mark_filter(date, student):
    simple_mark = MarkType.objects.get(pk=2)
    marks = Mark.objects.filter(student=student.id, date=date, type=simple_mark)
    if marks:
        return True
    return False


@register.simple_tag
def get_simple_mark(date, topic, student):
    simple_mark = MarkType.objects.get(pk=2)
    mark = Mark.objects.get(topic=topic, student=student.id, date=date, type=simple_mark)
    return mark.mark


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


@register.filter
def topical_mark(topic, student):
    type_mark = MarkType.objects.get(pk=1)
    return Mark.objects.get(student=student.id, topic=topic, type=type_mark).mark


@register.filter
def true(d):
    return True
