from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Логін'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Пароль'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError('Нема пользователя з таким ніком!')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не вірен!')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Пользователь неактивен!')
            return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            'placeholder': 'Логін'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Пароль ще раз', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                         'placeholder': 'Пароль'}))

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Паролi не однаковi!')
        return data['password2']

    class Meta:
        model = User
        fields = ('username',)
