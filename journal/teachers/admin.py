from django.contrib import admin
from teachers.models import Teacher, Subject, TeacherSubjects, ClassTeacher, MarkType, Mark, Topic


admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(TeacherSubjects)
admin.site.register(ClassTeacher)
admin.site.register(MarkType)
admin.site.register(Mark)
admin.site.register(Topic)
