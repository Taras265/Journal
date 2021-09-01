from django.urls import path
from teachers.views import home, journal_detail, mark_add, create_topic, \
    topical_mark_add, card, add_semester, remake_topic

urlpatterns = [
    path('', home, name='home'),
    path('journal/<int:pk>/', journal_detail, name='journal_marks'),
    path('journal/<int:pk>/add/mark/', mark_add, name='add_mark'),
    path('journal/<int:pk>/add/topic/', create_topic, name='add_topic'),
    path('journal/<int:pk>/add/topical_mark/', topical_mark_add,
         name='add_topical_mark'),
    path('journal/<int:pk>/card/', card, name='card'),
    path('journal/<int:pk>/card/add/semester/', add_semester, name='add_semester'),
    path('journal/<int:pk>/remake/topic/', remake_topic, name='remake_topic'),
]
