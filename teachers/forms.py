from django import forms
from django.contrib.auth.models import Group
from teachers.models import Subject, TeacherSubjects, Teacher, ClassTeacher, MarkType, \
    Mark, Topic, Semester
from students.models import SchoolJournal, ClassSubjects, Student

group = Group.objects.get(name='Вчитель')


class SubjectForm(forms.ModelForm):
    name = forms.CharField(label='Предмет', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'placeholder': 'Предмет'}))

    class Meta:
        model = Subject
        fields = ('name',)


class TeacherForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=group.user_set.all(),
                                     label='Додати користувачу',
                                     widget=forms.Select(attrs={'class': 'form-control',
                                                                'placeholder': 'Додати користувачу'}))
    name = forms.CharField(label="Iм'я", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                       'placeholder': "Iм'я"}))
    so_name = forms.CharField(label='Прізвище', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Прізвище'}))
    second_name = forms.CharField(label='По батькові', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                     'placeholder': 'По батькові'}))
    date = forms.DateField(label='Дата народження', widget=forms.DateInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Дата народження'}))
    address = forms.CharField(label='Адреса', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Адреса'}))

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSubjectsForm(forms.ModelForm):
    teacher_id = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='Додати вчителю',
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Додати користувачу'}))
    subjects = forms.ModelMultipleChoiceField(label='Предмети', queryset=Subject.objects.all(),
                                              widget=forms.SelectMultiple
                                              (attrs=
                                               {'class': 'form-control js-example-basic-multiple'}))

    class Meta:
        model = TeacherSubjects
        fields = ('subjects', 'teacher_id')


class FindTeacherForm(forms.ModelForm):
    subjects = forms.ModelChoiceField(label='Пошук по предметам', queryset=Subject.objects.all(),
                                      widget=forms.Select
                                      (attrs=
                                       {'class': 'form-control me-2'}))

    class Meta:
        model = TeacherSubjects
        fields = ('subjects',)


class ClassTeacherForm(forms.ModelForm):
    subject_id = forms.ModelChoiceField(label='Предмет', queryset=Subject.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Предмет'}))
    journal_id = forms.ModelChoiceField(label='Класс', queryset=SchoolJournal.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Класс'}))
    teacher_id = forms.ModelChoiceField(label='Вчитель', queryset=TeacherSubjects.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Вчитель'}))

    def clean(self):
        cleaned_data = super().clean()
        subject_id = self.cleaned_data.get("subject_id")
        journal_id = self.cleaned_data.get("journal_id")
        teacher_id = self.cleaned_data.get("teacher_id")
        if not ClassSubjects.objects.filter(class_num=journal_id.class_num):
            raise forms.ValidationError('Ви не додали предмети цієЇ паралелі!')
        class_subjects = ClassSubjects.objects.get(class_num=journal_id.class_num)
        if ClassTeacher.objects.filter(journal_id=journal_id, subject_id=subject_id):
            raise forms.ValidationError('Вже є такий вчитель у класі!')
        if not list(class_subjects.subjects.filter(name=str(subject_id))):
            raise forms.ValidationError('Предмет не вірен!')
        if not list(teacher_id.subjects.filter(name=subject_id.name)):
            raise forms.ValidationError('Вчитель не має таких предметів!')
        return cleaned_data

    class Meta:
        model = ClassTeacher
        fields = '__all__'


class AddMark(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.HiddenInput())
    mark = forms.IntegerField(label="Оцінка" + str(student.queryset), widget=forms.NumberInput(
        attrs=
        {'class': 'form-control'}))
    teacher = forms.ModelChoiceField(queryset=ClassTeacher.objects.all(), widget=forms.HiddenInput())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.HiddenInput())
    type = forms.ModelChoiceField(queryset=MarkType.objects.all(), widget=forms.HiddenInput())
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.HiddenInput(),
                                   required=False)

    class Meta:
        model = Mark
        fields = '__all__'


class TopicForm(forms.ModelForm):
    topic = forms.CharField(label="Тема", widget=forms.TextInput(attrs={'class': 'form-control',
                                                                        'placeholder': "Тема"}))

    start = forms.DateField(widget=forms.HiddenInput())
    finish = forms.DateField(widget=forms.HiddenInput(), required=False)
    class_teacher = forms.ModelChoiceField(queryset=ClassTeacher.objects.all(),
                                           widget=forms.HiddenInput())

    class Meta:
        model = Topic
        fields = ('topic', 'start', 'finish', 'class_teacher')


class SemesterForm(forms.ModelForm):
    start = forms.DateField(label='Дата початку',
                            widget=forms.DateInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Дата початку'}))
    finish = forms.DateField(label='Дата кінця',
                             widget=forms.DateInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Дата кінця'}))
    semester = forms.ModelChoiceField(label='Семестр',
                                      queryset=MarkType.objects.filter(pk__in=[3, 5]),
                                      widget=forms.Select(attrs={'class': 'form-control',
                                                                 'placeholder': 'Семестр'}))

    class Meta:
        model = Semester
        fields = '__all__'
