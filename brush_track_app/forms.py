
from django.contrib.auth.forms import UserCreationForm
from django import forms

from brush_track_app.models import Login, Client, Supervisor, Painter, Notification, FollowRequest, Work, Rating


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

class NotificationRegister(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter notification message here...'
            }),
        }

class followRequestRegister(forms.ModelForm):
    class Meta:
        model = FollowRequest
        fields = "__all__"


class WorkRegister(forms.ModelForm):

    class Meta:
        model = Work
        fields = ["location","work_type","square_feet","paint_type","start_date","expected_finish_date","budget",
        ]

        widgets = {



            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Location"
            }),

            "work_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "square_feet": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Square Feet"
            }),

            "paint_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Interior / Exterior"
            }),

            "start_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),

            "expected_finish_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),

            "budget": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Budget"
            }),
        }

class RatingRegister(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ["rating", "review"]

        widgets = {
            "rating": forms.Select(choices=[
                (1,"⭐ 1"),
                (2,"⭐⭐ 2"),
                (3,"⭐⭐⭐ 3"),
                (4,"⭐⭐⭐⭐ 4"),
                (5,"⭐⭐⭐⭐⭐ 5")
            ])
        }