from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect


@login_required
def home(request):
    u = User.objects.get(pk=request.user.id)
    if u.groups.filter(name='Секретар').exists():
        return redirect('/secretaries')
    elif u.groups.filter(name='Вчитель').exists():
        return redirect('/teachers')
    elif u.groups.filter(name='Учень').exists():
        return redirect('/students')
    return redirect('/admin')
