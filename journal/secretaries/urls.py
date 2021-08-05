from django.urls import path
from secretaries.views import home, add_teacher, TeacherInfoCreateView, TeacherSubjectsCreateView,\
    teacher_info_list, DeleteUserView, RefactorTeacherInfoView, RefactorTeacherSubjectsView,\
    SubjectCreateView, SubjectListView, RefactorSubjectView, DeleteSubjectView, add_student,\
    StudentInfoCreateView, JournalCreateView, student_info_list, JournalListView,\
    RefactorStudentInfoView, RefactorJournalView, DeleteJournalView, ClassSubjectsCreateView,\
    ClassSubjectsListView, RefactorClassSubjectsView, DeleteClassSubjectsView,\
    ClassTeacherCreateView, class_teacher_list, RefactorClassTeacherView, DeleteClassTeacherView

urlpatterns = [
    path('', home, name='home'),
    path('add/teacher/user/', add_teacher, name='add_teacher'),
    path('add/teacher/info/', TeacherInfoCreateView.as_view(), name='add_teacher_info'),
    path('add/teacher/subjects/', TeacherSubjectsCreateView.as_view(), name='add_teacher_subjects'),
    path('add/subject/', SubjectCreateView.as_view(), name='add_subject'),
    path('list/teacher/', teacher_info_list, name='teacher_list'),
    path('list/subject/', SubjectListView.as_view(), name='subject_list'),
    path('refactor/teacher/info/<int:pk>/', RefactorTeacherInfoView.as_view(), name='refactor_teacher'),
    path('refactor/teacher/subjects/<int:pk>/',
         RefactorTeacherSubjectsView.as_view(), name='refactor_subjects'),
    path('refactor/subject/<int:pk>/', RefactorSubjectView.as_view(), name='refactor_subject'),
    path('delete/user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('delete/subject/<int:pk>/', DeleteSubjectView.as_view(), name='delete_subject'),
    path('add/student/user/', add_student, name='add_student'),
    path('add/student/info/', StudentInfoCreateView.as_view(), name='add_student_info'),
    path('add/journal/', JournalCreateView.as_view(), name='add_journal'),
    path('list/student/', student_info_list, name='student_list'),
    path('list/journal/', JournalListView.as_view(), name='journal_list'),
    path('refactor/student/<int:pk>/', RefactorStudentInfoView.as_view(), name='refactor_student'),
    path('refactor/journal/<int:pk>/', RefactorJournalView.as_view(), name='refactor_journal'),
    path('delete/journal/<int:pk>/', DeleteJournalView.as_view(), name='delete_journal'),
    path('add/class_subjects/', ClassSubjectsCreateView.as_view(), name='add_class_subjects'),
    path('list/class_subjects/', ClassSubjectsListView.as_view(), name='class_subjects_list'),
    path('refactor/class_subjects/<int:pk>/', RefactorClassSubjectsView.as_view(),
         name='refactor_class_subjects'),
    path('delete/class_subjects/<int:pk>/', DeleteClassSubjectsView.as_view(),
         name='delete_class_subjects'),
    path('add/teacher_to_class/', ClassTeacherCreateView.as_view(), name='add_teacher_to_class'),
    path('list/teachers_class/', class_teacher_list, name='class_teacher_list'),
    path('refactor/teachers_class/<int:pk>/', RefactorClassTeacherView.as_view(),
         name='refactor_teacher_class'),
    path('delete/teachers_class/<int:pk>/', DeleteClassTeacherView.as_view(),
         name='delete_class_teacher'),
]
