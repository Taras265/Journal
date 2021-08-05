from django.contrib import admin
from django.urls import path
from teachers.views import home, journal_detail, mark_add, create_topic

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('journal/<int:pk>/', journal_detail, name='journal_marks'),
    path('journal/<int:pk>/add/mark/', mark_add, name='add_mark'),
    path('journal/<int:pk>/add/topic/', create_topic, name='add_topic'),
]
