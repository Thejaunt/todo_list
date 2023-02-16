from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Task


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=200, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=True,
                                widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', strip=False, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm password', strip=False, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 10, 'id': 'floatingTextarea2', 'style': "height: 500px"})
        }


