from django.urls import path
from students.views import journal_detail, card, home

urlpatterns = [
    path('', home, name='home'),
    path('subject/<int:pk>/', journal_detail, name='journal_marks'),
    path('card/', card, name='card'),
]
