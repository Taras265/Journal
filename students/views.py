from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from teachers.models import ClassTeacher, Teacher, TeacherSubjects, Mark, \
    SchoolJournal, Student, Subject, MarkType
import datetime
from teachers.models import Topic
from students.models import ClassSubjects
from django.contrib import messages

now = datetime.datetime.now()


@login_required()
def home(request):
    user = request.user
    user_student = Student.objects.get(user_id=user)
    subjects_class = ClassSubjects.objects.get(class_num=user_student.journal_id.class_num)
    subjects = []
    for subject in subjects_class.subjects.all():
        subjects.append(subject)
    return render(request, 'students/home.html', {'subjects': subjects})


@login_required()
def journal_detail(request, pk=None):
    if pk:
        user = request.user
        user_student = Student.objects.get(user_id=user)
        context = {}
        subject = Subject.objects.get(pk=pk)
        if len(ClassTeacher.objects.filter(subject_id=subject,
                                           journal_id=user_student.journal_id)) >= 2:
            class_teacher = ClassTeacher.objects.filter(subject_id=subject,
                                                        journal_id=user_student.journal_id, group=user_student.group)
        else:
            class_teacher = ClassTeacher.objects.filter(subject_id=subject,
                                                        journal_id=user_student.journal_id)
        if not class_teacher:
            messages.error(request, 'Ще немає вчителя цього предмету!')
            return redirect('/students')
        else:
            class_teacher = class_teacher[0]
            topics = []
            topic_list = []
            for i in Topic.objects.filter(class_teacher=class_teacher):
                topic_list.append(i.id)
                topics.append(i)
            if topic_list:
                topic_list = max(topic_list)
            else:
                topic_list = 1
            page = request.GET.get('topic') or topic_list
            topic = Topic.objects.filter(pk=int(page))
            if topic:
                topic = topic[0]
                dates = set()
                marks_not_clear = Mark.objects.filter(teacher=class_teacher,
                                                      subject=class_teacher.subject_id,
                                                      topic=topic,
                                                      student=user_student)
                if marks_not_clear:
                    table = True
                else:
                    table = False
                for mark in marks_not_clear:
                    if mark.type != MarkType.objects.get(pk=1):
                        dates.add(mark.date)
                dates = sorted(dates)
                context.update({'dates': dates, 'topics': topics, 'page': topic,
                                'class_teacher': class_teacher,
                                'student': user_student,
                                'table': table})
            else:
                context.update({'topics': topics, 'class_teacher': class_teacher,
                                'student': user_student})
            return render(request, 'students/journal_detail.html', context)


@login_required
def card(request):
    user = request.user
    user_student = Student.objects.get(user_id=user)
    subjects = list()
    first_year = MarkType.objects.get(pk=3)
    second_year = MarkType.objects.get(pk=5)
    all_year = MarkType.objects.get(pk=4)
    first = list()
    for mark in Mark.objects.filter(type=first_year, student=user_student):
        first.append(mark)
    second = list()
    for mark in Mark.objects.filter(type=second_year, student=user_student):
        second.append(mark)
    year = list()
    for mark in Mark.objects.filter(type=all_year, student=user_student):
        year.append(mark)
    class_subjects = ClassSubjects.objects.get(class_num=user_student.journal_id.class_num)
    for subject in class_subjects.subjects.all():
        subjects.append(subject)
    data = {'first': first,
            'second': second,
            'year': year,
            'student': Student.objects.get(pk=user_student.pk),
            'subjects': list(subjects)}
    return render(request, 'students/card.html', data)
