import random

import pandas
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from accounts.forms import UserRegistrationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from teachers.forms import TeacherForm, TeacherSubjectsForm, SubjectForm, \
    ClassTeacherForm, FindTeacherForm
from teachers.models import Teacher, TeacherSubjects, Subject, ClassTeacher
from students.forms import StudentForm, JournalForm, ClassSubjectsForm, FindStudentForm
from students.models import Student, SchoolJournal, ClassSubjects


@login_required
def home(request):
    return render(request, 'secretaries/home.html')


@login_required
def add_teacher(request):
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(random.randint(8, 15)):
        password += random.choice(chars)
    data = request.method
    if data == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name='Вчитель')
            group.user_set.add(new_user)
            messages.success(request, 'Вчителя додано!'
                                      ' Не забудьте ввести додаткову інформацію!')
            return redirect('/secretaries/add/teacher/info')
        return render(request, 'secretaries/create.html', {'form': form})
    else:
        form = UserRegistrationForm(initial={
            'password': password
        })
        return render(request, 'secretaries/create.html', {'form': form})


@login_required
def add_student(request):
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range(random.randint(8, 15)):
        password += random.choice(chars)
    data = request.method
    if data == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            group = Group.objects.get(name='Учень')
            group.user_set.add(new_user)
            messages.success(request, 'Учня додано!'
                                      ' Не забудьте ввести додаткову інформацію!')
            return redirect('/secretaries/add/student/info')
        return render(request, 'secretaries/create.html', {'form': form})
    else:
        form = UserRegistrationForm(initial={
            'password': password,
        })
        return render(request, 'secretaries/create.html', {'form': form})


class TeacherInfoCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'secretaries/create.html'
    success_message = "Інформація про вчителя записана!"
    success_url = '/secretaries/add/teacher/subjects'


class StudentInfoCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'secretaries/create.html'
    success_message = "Інформація про учня записана!"
    success_url = '/secretaries/'


class TeacherSubjectsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = TeacherSubjects
    form_class = TeacherSubjectsForm
    template_name = 'secretaries/create.html'
    success_message = "Предмети вчителя додані!"
    success_url = '/secretaries/'


class SubjectCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'secretaries/create.html'
    success_message = "Предмет додано!"
    success_url = '/secretaries/'


class JournalCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = SchoolJournal
    form_class = JournalForm
    template_name = 'secretaries/create.html'
    success_message = "Журнал додан!"
    success_url = '/secretaries/'


class ClassSubjectsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ClassSubjects
    form_class = ClassSubjectsForm
    template_name = 'secretaries/create.html'
    success_message = "Предмети, які викладають в класі, додано!"
    success_url = '/secretaries/'


class ClassTeacherCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = ClassTeacher
    form_class = ClassTeacherForm
    template_name = 'secretaries/create.html'
    success_message = "Вчитель викладає в новому класі!"
    success_url = '/secretaries/'


@login_required()
def teacher_info_list(request):
    if request.method == 'POST':
        form = FindTeacherForm(request.POST)
        qs = TeacherSubjects.objects.all()
        lst = Paginator(qs, 15)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        context = {'page_obj': page_obj, 'form': form,
                   'all': qs}
        if form.is_valid():
            try:
                qs = []
                for i in TeacherSubjects.objects.all():
                    if form.cleaned_data['subjects'] in list(i.subjects.all()):
                        qs.append(i)
                if not qs:
                    qs = TeacherSubjects.objects.all()
                    messages.error(request, 'Такого вчителя немає!')
                lst = Paginator(qs, 15)
                page_number = request.GET.get('page')
                page_obj = lst.get_page(page_number)
                context = {'page_obj': page_obj, 'form': form,
                           'all': qs}
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'secretaries/teacher_list.html', context)
            return render(request, 'secretaries/teacher_list.html', context)
        return render(request, 'secretaries/teacher_list.html', context)
    else:
        qs = TeacherSubjects.objects.all()
        form = FindTeacherForm()
        lst = Paginator(qs, 15)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        context = {'page_obj': page_obj, 'form': form,
                   'all': qs}
        return render(request, 'secretaries/teacher_list.html', context)


class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    paginate_by = 15
    template_name = 'secretaries/subject_list.html'


@login_required()
def student_info_list(request):
    if request.method == 'POST':
        form = FindStudentForm(request.POST)
        qs = Student.objects.all()
        lst = Paginator(qs, 15)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        context = {'page_obj': page_obj, 'form': form,
                   'all': qs}
        if form.is_valid():
            try:
                qs = Student.objects.filter(journal_id=form.cleaned_data['journal_id'])
                if not qs:
                    qs = Student.objects.all()
                    messages.error(request, 'Такого учня немає!')
                lst = Paginator(qs, 15)
                page_number = request.GET.get('page')
                page_obj = lst.get_page(page_number)
                context = {'page_obj': page_obj, 'form': form,
                           'all': qs}
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'secretaries/student_list.html', context)
            return render(request, 'secretaries/student_list.html', context)
        return render(request, 'secretaries/student_list.html', context)
    else:
        qs = Student.objects.all()
        form = FindStudentForm()
        lst = Paginator(qs, 15)
        page_number = request.GET.get('page')
        page_obj = lst.get_page(page_number)
        context = {'page_obj': page_obj, 'form': form,
                   'all': qs}
        return render(request, 'secretaries/student_list.html', context)


class JournalListView(LoginRequiredMixin, ListView):
    model = SchoolJournal
    paginate_by = 15
    template_name = 'secretaries/journal_list.html'


@login_required()
def class_teacher_list(request):
    qs = ClassTeacher.objects.all()
    context = {'class_teachers': qs}
    return render(request, 'secretaries/class_teacher_list.html', context)


class ClassSubjectsListView(LoginRequiredMixin, ListView):
    model = ClassSubjects
    template_name = 'secretaries/class_subjects_list.html'


class RefactorTeacherInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Інформація про вчителя змінена!"


class RefactorClassSubjectsView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ClassSubjects
    form_class = ClassSubjectsForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Предмети, які викладаються в класі, змінені!"


class RefactorSubjectView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Предмет змінено!"


class RefactorTeacherSubjectsView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = TeacherSubjects
    form_class = TeacherSubjectsForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Предмети, які викладає вчитель, змінені!"


class RefactorStudentInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Інформація про учня змінена!"


class RefactorJournalView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SchoolJournal
    form_class = JournalForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Журнал змінено!"


class RefactorClassTeacherView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = ClassTeacher
    form_class = ClassTeacherForm
    template_name = 'secretaries/refactor.html'
    success_url = reverse_lazy('secretaries:home')
    success_message = "Вчителя змінено!"


class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('secretaries:home')
    template_name = 'secretaries/delete.html'
    success_message = 'Користувач видален!'


class DeleteSubjectView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('secretaries:home')
    template_name = 'secretaries/delete.html'
    success_message = 'Предмет видален!'


class DeleteJournalView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy('secretaries:home')
    template_name = 'secretaries/delete.html'
    success_message = 'Журнал видален!'


class DeleteClassSubjectsView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassSubjects
    success_url = reverse_lazy('secretaries:home')
    template_name = 'secretaries/delete.html'
    success_message = 'Предмети, які викладаються в класі видалено!'


class DeleteClassTeacherView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassTeacher
    success_url = reverse_lazy('secretaries:home')
    template_name = 'secretaries/delete.html'
    success_message = 'Вчителя классу видалено!'


def load_students(request):
    if request.method == 'POST':
        data = dict(request.FILES)
        if 'file' in data:
            try:
                data = pandas.read_excel(data['file'][0])
                for i in range(0, data['ID'].iloc[-1]):
                    form = UserRegistrationForm({'username': data['Login'].iloc[i],
                                                 'password': data['Password'].iloc[i],
                                                 'password2': data['Password'].iloc[i],
                                                 'email': data['Email'].iloc[i]})
                    new_user = form.save(commit=False)
                    new_user.set_password(form.cleaned_data['password'])
                    new_user.save()
                    group = Group.objects.get(name='Учень')
                    group.user_set.add(new_user)
                    user = User.objects.get(username=data['Login'].iloc[-1])
                    journal = SchoolJournal.objects.get(class_num=int(data['Journal'].iloc[i][0]),
                                                        class_letter=data['Journal'].iloc[i][1])
                    info = StudentForm({'user_id': user, 'journal_id': journal,
                                        'name': data['Name'].iloc[i],
                                        'so_name': data['Surname'].iloc[i],
                                        'second_name': data['Second name'].iloc[i],
                                        'date': data['Date'].iloc[i],
                                        'address': data['Address'].iloc[i],
                                        'group': data['Group'].iloc[i]})
                    info.save()
                messages.success(request, 'Учні додані!')
            except:
                messages.error(request, 'Помилка! Перевірте таблицю! Данні збереженні до '+str(i) + ' ID!')
            return redirect('/secretaries/')
    return render(request, 'secretaries/load.html')
