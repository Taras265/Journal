from django import forms
from django.contrib.auth.models import Group
from students.models import SchoolJournal, Student, ClassSubjects
from teachers.models import Teacher

from teachers.models import Subject

group = Group.objects.get(name='Учень')


class StudentForm(forms.ModelForm):
    user_id = forms.ModelChoiceField(queryset=group.user_set.all(),
                                     label='Додати користувачу',
                                     widget=forms.Select(attrs={'class': 'form-control',
                                                                'placeholder': 'Додати користувачу'}))
    journal_id = forms.ModelChoiceField(queryset=SchoolJournal.objects.all(), label='Додати до журналу',
                                        widget=forms.Select(attrs={'class': 'form-control',
                                                                   'placeholder': 'Додати до журналу'}))
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
        model = Student
        fields = '__all__'


class FindStudentForm(forms.ModelForm):
    journal_id = forms.ModelChoiceField(queryset=SchoolJournal.objects.all(), label='Шукати по журналу',
                                        widget=forms.Select
                                        (attrs={'class': 'form-control me-2'}))

    class Meta:
        model = Student
        fields = ('journal_id',)


class JournalForm(forms.ModelForm):
    class_num = forms.IntegerField(label="Номер классу", widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                                         'placeholder': "Номер классу"}))
    class_letter = forms.CharField(label='Буква классу', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Буква классу'}))
    year = forms.DateField(label='Навчальний рік', widget=forms.DateInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Навчальний рік'}))
    class_teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), label='Додати класного керівника',
                                           widget=forms.Select(attrs={'class': 'form-control',
                                                                      'placeholder': 'Додати класного кірівника'}))

    def clean_class_num(self):
        num = self.cleaned_data.get('class_num')
        if int(num) > 11:
            raise forms.ValidationError('Номер классу не вірен!')
        return num

    class Meta:
        model = SchoolJournal
        fields = '__all__'


class ClassSubjectsForm(forms.ModelForm):
    class_num = forms.IntegerField(label="Номер классу", widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'placeholder': 'Номер классу'}))
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), label='Додати предмети',
                                              widget=forms.SelectMultiple
                                              (attrs=
                                               {'class': 'form-control js-example-basic-multiple'}))

    def clean_class_num(self):
        num = self.cleaned_data.get('class_num')
        if int(num) > 11:
            raise forms.ValidationError('Номер классу не вірен!')
        return num

    def clean_subjects(self):
        subjects = self.cleaned_data.get('subjects')
        return subjects

    class Meta:
        model = ClassSubjects
        fields = '__all__'
