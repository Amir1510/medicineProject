from django.shortcuts import render, redirect
from medicine_app.forms import *
from medicine_app.models import *
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'o_nas.html')
def donors(request):
    return render(request, 'kak_stat_donorom.html')
def logining(request):
    return render(request, 'login.html')
def profile(request):
    return render(request, 'profile.html')

def get_blood_date(request):
    username = request.user.username
    filtered_data = Plan.objects.filter(username=username)
    filtered_data2 = CreateUser.objects.filter(username=username)

    return render(request, 'profile.html', {'filtered_data': filtered_data, 'filtered_data2': filtered_data2})


class PlanView(View):

    def get(self, request):
        form = Appointment()
        return render(request, 'planirovanie.html', context={
            'form': form,
        })

    def post(self,request):
        if request.method == 'POST':
            form = Appointment(request.POST)
            if form.is_valid():
                blood_date = form.save(commit=False)
                blood_date.username = request.user.username
                blood_date.save()
                return redirect('/profile/')
        else:
            form = Appointment()

        return render(request, 'planirovanie.html', {'form': form})



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'register.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                user.save()
                return HttpResponseRedirect('/')
        return render(request, 'register.html', context={
            'form': form,
        })
class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'login.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, "Неправильный пароль или указанная учётная запись не существует!")
                return render(request, "login.html", {"form": form})
        return render(request, 'login.html', context={
            'form': form,
        })