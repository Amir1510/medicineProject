from django import forms
from medicine_app.models import *
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.shortcuts import render




class SignInForm(forms.Form):
    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputEmail",
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
        })
    )

class Appointment(ModelForm):
    class Meta:
        model = Plan
        fields = ['group_of_blood', 'age', 'height', 'weight']


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'type': 'username',
        }),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputEmail",
            'type': 'email',
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'type': 'password',
        }),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
            'type': 'password',
        }),
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароли не совпадают"
            )
    def clean_username(self):
        username = self.cleaned_data['username']
        if CreateUser.objects.filter(username=username).exists():
            print(username)
            raise forms.ValidationError("Пользователь с таким name уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if CreateUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email



    def save(self):
        user = CreateUser(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth