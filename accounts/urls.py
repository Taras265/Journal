from django.urls import path
from accounts.views import login_view, logout_view, change_password

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change/', change_password, name='change_password'),
]