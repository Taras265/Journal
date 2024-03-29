from math import ceil

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from students.models import ClassSubjects
from teachers.models import ClassTeacher, Teacher, TeacherSubjects, Mark, \
    SchoolJournal, Student, Subject, MarkType
from teachers.forms import AddMark, TopicForm, SemesterForm, AddMarkBy
import datetime
from teachers.models import Topic

now = datetime.datetime.now()


@login_required()
def home(request):
    user_id = request.user.id
    info_id = Teacher.objects.filter(user_id=user_id)
    if info_id:
        teacher_id = TeacherSubjects.objects.get(teacher_id=info_id[0])
        journals = ClassTeacher.objects.filter(teacher_id=teacher_id)
        return render(request, 'teachers/home.html', {'journals': journals})
    return render(request, 'teachers/home.html')


@login_required()
def journal_detail(request, pk=None):
    if pk:
        context = {'form': ""}
        if request.method == 'POST':
            data = request.POST
            if data:
                if 'student' in data:
                    student = Student.objects.get(pk=int(data['student']))
                    date = data['date']
                    teacher = ClassTeacher.objects.get(pk=int(data['teacher']))
                    subject = Subject.objects.get(pk=int(data['subject']))
                    type_mark = MarkType.objects.get(pk=2)
                    form = AddMark(initial={
                        'student': student,
                        'date': date,
                        'teacher': teacher,
                        'subject': subject,
                        'type': type_mark,
                        'topic': Topic.objects.get(pk=int(data['topic']))
                    })
                    context['form'] = form
                    context['student'] = student
                else:
                    teacher = ClassTeacher.objects.get(pk=int(data['teacher']))
                    subject = Subject.objects.get(pk=int(data['subject']))
                    type_mark = MarkType.objects.get(pk=2)
                    form = AddMarkBy(initial={
                        'teacher': teacher,
                        'subject': subject,
                        'type': type_mark,
                        'topic': Topic.objects.get(pk=int(data['topic']))
                    })
                    context['form'] = form
        class_teacher = ClassTeacher.objects.get(id=pk)
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
            heads = set()
            marks_not_clear = Mark.objects.filter(teacher=class_teacher,
                                                  subject=class_teacher.subject_id,
                                                  topic=topic)
            print_tf = False
            for mark in marks_not_clear:
                print_tf = True
                if mark.type != MarkType.objects.get(pk=1):
                    dates.add(mark.date)
                    heads.add(mark.date.strftime("%d.%m.%y"))
            dates = sorted(dates)
            heads = sorted(heads)
            if topic.finish:
                heads.append('Тематична')
            elif now.strftime("%d.%m.%y") not in heads:
                heads.append('Сьогодні')
            if class_teacher.group:
                students = Student.objects.filter(journal_id=class_teacher.journal_id.id, group=class_teacher.group)
            else:
                students = Student.objects.filter(journal_id=class_teacher.journal_id.id)
            context.update({'students': students,
                            'dates': dates, 'topics': topics, 'page': topic,
                            'class_teacher': class_teacher, 'heads': heads,
                            'print': print_tf
                            })
        else:
            context.update({'topics': topics, 'class_teacher': class_teacher,
                            'print': False})
        return render(request, 'teachers/journal_detail.html', context)


@login_required
def mark_add(request, pk):
    if pk:
        if request.method == 'POST':
            data = request.POST.copy()
            if not AddMark(data).is_valid():
                data['date'] = now.date()
            form = AddMark(data)
            if form.is_valid():
                if not Topic.objects.get(pk=int(request.POST.copy()['topic'])).finish:
                    dates = []
                    for mark in Mark.objects.filter(student=request.POST.copy()['student']):
                        dates.append(mark.date)
                    if request.POST.copy()['date'] not in dates:
                        form.save()
                        messages.success(request, "Оцінка збережена")
                        return redirect('/teachers/journal/' + str(pk) + '/')
                    messages.error(request, "За цей день вже є така оцінка!")
                    return redirect('/teachers/journal/' + str(pk) + '/')
                messages.error(request, "Тема закінчена!")
                return redirect('/teachers/journal/' + str(pk) + '/')
            messages.error(request, "Ви не усе ввели для додання оцінки, або данні не верні!")
            return redirect('/teachers/journal/' + str(pk) + '/')
        messages.error(request, "Нема данних для додання оцінки!!")
        return redirect('/teachers/journal/' + str(pk) + '/')


@login_required
def create_topic(request, pk=None):
    if pk:
        if request.method == 'POST':
            data = request.POST
            form = TopicForm(data)
            if form.is_valid():
                form.save()
                messages.success(request, "Тема додана!")
                return redirect('/teachers/journal/' + str(pk) + '/')
            elif data:
                class_teacher = ClassTeacher.objects.get(pk=int(data['class_teacher']))
                start = now.date()
                form = TopicForm(initial={
                    'class_teacher': class_teacher,
                    'start': start,
                })
                return render(request, 'teachers/create.html', {'form': form})


@login_required
def remake_topic(request, pk=None):
    if pk:
        if request.method == 'POST':
            data = request.POST
            if 'save' not in data:
                model = Topic.objects.get(id=data['id'])
                model.topic = data['input']
                model.save()
                messages.success(request, 'Тема змінена!')
                return redirect('/teachers/journal/' + str(pk) + '/')
            else:
                model = Topic.objects.get(pk=int(data['save']))
            return render(request, 'teachers/reform.html', {'input': model.topic,
                                                            'id': model.id})
        else:
            messages.error(request, 'Нема данних!')
        return redirect('/teachers/journal/' + str(pk) + '/')


@login_required
def topical_mark_add(request, pk=None):
    if pk:
        if request.method == 'POST':
            data_form = request.POST.copy()
            data_form['date'] = now.date()
            data_form['teacher'] = ClassTeacher.objects.get(pk=int(data_form['teacher']))
            data_form['subject'] = Subject.objects.get(pk=data_form['subject'])
            data_form['topic'] = Topic.objects.get(pk=data_form['topic'])
            data_form['type'] = MarkType.objects.get(pk=1)
            class_teacher = ClassTeacher.objects.get(id=pk)
            if class_teacher.group:
                students = Student.objects.filter(journal_id=class_teacher.journal_id.id, group=class_teacher.group)
            else:
                students = Student.objects.filter(journal_id=class_teacher.journal_id.id)
            for student in students:
                mark_sum = 0
                data_form['student'] = student
                for mark in Mark.objects.filter(student=student.id,
                                                topic=data_form['topic']):
                    mark_sum += int(mark.mark)
                if mark_sum != 0:
                    data_form['mark'] = ceil(mark_sum / len(list(Mark.objects.filter(student=student.id,
                                                                                     topic=data_form['topic']))))
                else:
                    data_form['mark'] = 0
                if not Topic.objects.get(id=data_form['topic'].id).finish:
                    mark_form = AddMark(data_form)
                    mark_form.save()
                    messages.success(request, "Тематична оцінка збережена!")
            Topic.objects.filter(id=data_form['topic'].id).update(finish=data_form['date'])
        return redirect('/teachers/journal/' + str(pk) + '/')


@login_required
def card(request, pk=None):
    if pk:
        class_teacher = ClassTeacher.objects.get(id=pk)
        first_year = MarkType.objects.get(pk=3)
        second_year = MarkType.objects.get(pk=5)
        year = MarkType.objects.get(pk=4)
        if 0 < len(list(Mark.objects.filter(
                teacher=ClassTeacher.objects.get(id=pk).id,
                type__in=[MarkType.objects.get(pk=3),
                          MarkType.objects.get(pk=5)]))) % 2 == 0:
            semester = False
        else:
            semester = True
        if class_teacher.group:
            students = Student.objects.filter(journal_id=class_teacher.journal_id.id, group=class_teacher.group)
        else:
            students = Student.objects.filter(journal_id=class_teacher.journal_id.id)
        data = {'first': list(Mark.objects.filter(type=first_year, teacher=pk)),
                'second': Mark.objects.filter(type=second_year, teacher=pk),
                'year': Mark.objects.filter(type=year, teacher=pk),
                'class_teacher': class_teacher,
                'students': students,
                'semester': semester}
        return render(request, 'teachers/card.html', data)


@login_required
def add_semester(request, pk=None):
    if pk:
        if request.method == 'POST':
            teacher = ClassTeacher.objects.get(id=pk)
            if not Mark.objects.filter(teacher=teacher.id,
                                       type=request.POST.copy()['semester']):
                data = {
                    'date': now.date(),
                    'teacher': teacher,
                    'subject': teacher.subject_id,
                    'type': MarkType.objects.get(pk=int(request.POST.copy()['semester'][0]))
                }
                if teacher.group:
                    students = Student.objects.filter(journal_id=teacher.journal_id.id, group=teacher.group)
                else:
                    students = Student.objects.filter(journal_id=teacher.journal_id.id)
                for student in students:
                    if len(list(Mark.objects.filter(
                            student=student,
                            type=MarkType.objects.get(pk=1),
                            teacher=ClassTeacher.objects.get(id=pk).id))) <= 0:
                        messages.error(request, 'Нема тематичних оцінок!')
                        return redirect('/teachers/journal/' + str(pk) + '/card/')
                    data['student'] = student
                    mark_sum = 0
                    for mark in Mark.objects.filter(student=student,
                                                    type=MarkType.objects.get(pk=1),
                                                    teacher=ClassTeacher.objects.get(id=pk).id):
                        mark_sum += int(mark.mark)
                    if mark_sum > 0:
                        mark_sum = ceil(mark_sum / len(list(Mark.objects.filter(
                            student=student,
                            type=MarkType.objects.get(pk=1),
                            teacher=ClassTeacher.objects.get(id=pk).id))))
                    else:
                        mark_sum = 0
                    data['mark'] = mark_sum
                    form_mark = AddMark(data)
                    if form_mark.is_valid():
                        form_mark.save()
                    if len(list(Mark.objects.filter(
                            student=student,
                            teacher=ClassTeacher.objects.get(id=pk).id,
                            type__in=[MarkType.objects.get(pk=3),
                                      MarkType.objects.get(pk=5)]))) % 2 == 0:
                        data['type'] = MarkType.objects.get(pk=4)
                        mark_sum = 0
                        for mark in (Mark.objects.filter(
                                student=student,
                                type__in=[MarkType.objects.get(pk=3),
                                          MarkType.objects.get(pk=5)],
                                teacher=ClassTeacher.objects.get(id=pk).id)):
                            mark_sum += int(mark.mark)
                        if mark_sum > 0:
                            mark_sum = ceil(mark_sum / len(list(Mark.objects.filter(
                                student=student,
                                type__in=[MarkType.objects.get(pk=3),
                                          MarkType.objects.get(pk=5)],
                                teacher=ClassTeacher.objects.get(id=pk).id))))
                        else:
                            mark_sum = 0
                        data['mark'] = mark_sum
                        form_mark = AddMark(data)
                        if form_mark.is_valid():
                            form_mark.save()
                        data['type'] = MarkType.objects.get(
                            pk=int(request.POST.copy()['semester'][0]))
            else:
                messages.error(request, 'Ви вже поставили оцінку за цей період!')
            return redirect('/teachers/journal/' + str(pk) + '/card/')
        form = SemesterForm()
        return render(request, 'teachers/create.html', {'form': form})


def my_class(request):
    user = request.user
    teacher = Teacher.objects.get(user_id=user.pk)
    if not SchoolJournal.objects.filter(class_teacher=teacher):
        messages.error(request, 'Ви не класний керівник!')
        return redirect('/teachers/')
    teacher_s = TeacherSubjects.objects.get(teacher_id=teacher.id)
    class_teacher = ClassTeacher.objects.get(teacher_id=teacher_s.id)
    journal = SchoolJournal.objects.get(class_teacher=teacher)
    subjects_class = ClassSubjects.objects.get(class_num=journal.class_num)
    subjects = []
    for subject in subjects_class.subjects.all():
        ct = ClassTeacher.objects.filter(journal_id=journal.id, subject_id=subject.id)
        if ct:
            subjects.append(ct[0])
    students = Student.objects.filter(journal_id=class_teacher.journal_id.id)
    student = list(students)
    return render(request, 'teachers/class.html', {'subjects': subjects, 'students': student})


def class_card(request, pk):
    if pk:
        user_student = Student.objects.filter(id=pk)
        if user_student:
            user_student = user_student[0]
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
                    'subjects': list(subjects), }
            return render(request, 'teachers/class_card.html', data)
        messages.error(request, 'Нема такого учня!')
        return redirect('/teachers/')


def class_subject(request, pk):
    if pk:
        context = {'form': ""}
        class_teacher = ClassTeacher.objects.get(id=pk)
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
            heads = set()
            marks_not_clear = Mark.objects.filter(teacher=class_teacher,
                                                  subject=class_teacher.subject_id,
                                                  topic=topic)
            print_tf = False
            for mark in marks_not_clear:
                print_tf = True
                if mark.type != MarkType.objects.get(pk=1):
                    dates.add(mark.date)
                    heads.add(mark.date.strftime("%d.%m.%y"))
            dates = sorted(dates)
            heads = sorted(heads)
            if topic.finish:
                heads.append('Тематична')
            elif now.strftime("%d.%m.%y") not in heads:
                heads.append('Сьогодні')
            students = Student.objects.filter(journal_id=class_teacher.journal_id.id)
            context.update({'students': students,
                'dates': dates, 'topics': topics, 'page': topic,
                'class_teacher': class_teacher, 'heads': heads,
                'print': print_tf
            })
        else:
            context.update({'topics': topics, 'class_teacher': class_teacher,
                            'print': False})
        return render(request, 'teachers/class_subject.html', context)
