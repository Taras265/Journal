import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from accounts.forms import UserLoginForm
import smtplib


def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        _next = _next or '/'
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def change_password(request):
    code = random.randint(1111, 9999)
    part = '1'
    username = ''
    if request.method == 'POST':
        data = request.POST
        part = data['part']
        username = data['name']
        user = User.objects.get(username=username)
        if part == '2':
            code = data['code']
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            smtpObj.login('journal.for.school100@gmail.com', '/1/z/2/x/')
            smtpObj.sendmail("journal.for.school100@gmail.com", user.email, 'Your code - '+str(code))
            code = data['code']
            part = '3'
        elif part == '4':
            if data['code'] != data['ccode']:
                messages.error(request, 'Введiть правельний код!')
                part = '3'
            if not len(data['password']) >= 8:
                messages.error(request, 'Пароль должен вмiщувати 8, або бiльше символiв!')
                part = '3'
            if part == '4':
                user.set_password(data['password'])
                user.save()
                messages.success(request, 'Пароль змiнен!')
                return redirect('/accounts/login')
    return render(request, 'accounts/change_password.html', {'code': code, 'part': part, 'name': username})
