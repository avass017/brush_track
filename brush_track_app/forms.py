
from django.contrib.auth.forms import UserCreationForm
from django import forms

from brush_track_app.models import Login, Client, Supervisor, Painter


class LoginRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Login

        fields = ('username', 'password1', 'password2')


class clientRegister(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name','email','phone','address','document')

class supervisorRegister(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ('name','email','phone','address','document','id_proof','experience_years','is_active')

class painterRegister(forms.ModelForm):
    class Meta:
        model = Painter
        fields = ('supervisor','name','email','phone','address','document','experience_years')
