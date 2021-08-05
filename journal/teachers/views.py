from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from teachers.models import ClassTeacher, Teacher, TeacherSubjects, Mark,\
    SchoolJournal, Student, Subject, MarkType
from teachers.forms import AddMark, TopicForm
import datetime
from teachers.models import Topic

now = datetime.datetime.now()


@login_required()
def home(request):
    user_id = request.user.id
    info_id = Teacher.objects.get(user_id=user_id)
    teacher_id = TeacherSubjects.objects.get(teacher_id=info_id)
    journals = ClassTeacher.objects.filter(teacher_id=teacher_id)
    return render(request, 'teachers/home.html', {'journals': journals})


@login_required()
def journal_detail(request, pk=None):
    if pk:
        context = {'form': ""}
        if request.method == 'POST':
            data = request.POST
            if data:
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
                    'type': type_mark
                })
                context['form'] = form
        class_teacher = ClassTeacher.objects.get(id=pk)
        dates = set()
        marks_not_clear = Mark.objects.filter(teacher=class_teacher,
                                              subject=class_teacher.subject_id)
        for mark in marks_not_clear:
            dates.add(mark.date)
        context.update({'object': class_teacher,
                        'students': Student.objects.filter(journal_id=class_teacher.journal_id.id),
                        'dates': sorted(dates)})
        return render(request, 'teachers/journal_detail.html', context)


@login_required
def mark_add(request, pk):
    if pk:
        if request.method == 'POST':
            form = AddMark(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Оцінка збережена")
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
                form.save(commit=False)
                form.class_teacher = ClassTeacher.objects.get(pk=int(data['class_teacher']))
                print(form.class_teacher)
                form.save()
                messages.success(request, "Тема додана!!!")
                return redirect('/teachers/journal/' + str(pk) + '/')
            elif data:
                class_teacher = ClassTeacher.objects.get(pk=int(data['class_teacher']))
                start = now.date()
                form = TopicForm(initial={
                    'class_teacher': class_teacher,
                    'start': start,
                    'finish': start,
                })
                return render(request, 'teachers/create.html', {'form': form})
