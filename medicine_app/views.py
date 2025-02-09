from django.shortcuts import render, redirect
from medicine_app.forms import *
from medicine_app.models import *
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'o_nas.html')

def donors(request):
    return render(request, 'kak_stat_donorom.html')

def logining(request):
    return render(request, 'login.html')

@login_required
def profile(request):
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

    def post(self, request):
        if request.method == 'POST':
            form = Appointment(request.POST)
            if form.is_valid():
                username = request.user.username
                blood_date = form.save(commit=False)
                blood_date.username = username
                try:
                    blood_date.save()
                except:
                    model = Plan.objects.get(username=username)
                    model.weight = blood_date.weight
                    model.height = blood_date.height
                    model.age = blood_date.age
                    model.group_of_blood = blood_date.group_of_blood
                    model.save()
                return redirect('schedule_donation')
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

@login_required
def schedule_donation(request):
    if request.method == 'POST':
        donation_date = request.POST.get('donation_date')
        donation_time = request.POST.get('donation_time')
        
        if donation_date and donation_time:
            # Здесь вы можете добавить логику для сохранения запланированной донации
            # Например, создать новую запись в базе данных или обновить существующую
            
            messages.success(request, '')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, выберите дату и время донации')
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    hours = range(9, 19)
    minutes = ['00', '15', '30', '45']
    
    return render(request, 'schedule_donation.html', {
        'today_date': today_date,
        'hours': hours,
        'minutes': minutes
    })

@login_required
def check_donor_info(request):
    username = request.user.username
    donor_info = Plan.objects.filter(username=username).first()
    if donor_info:
        return redirect('schedule_donation')
    else:
        return redirect('planing_donor')

@login_required
def update_donor_info(request):
    if request.method == 'POST':
        form = Appointment(request.POST)
        if form.is_valid():
            username = request.user.username
            try:
                model = Plan.objects.get(username=username)
                model.weight = form.cleaned_data['weight']
                model.height = form.cleaned_data['height']
                model.age = form.cleaned_data['age']
                model.group_of_blood = form.cleaned_data['group_of_blood']
                model.save()
                messages.success(request, '')
            except Plan.DoesNotExist:
                blood_date = form.save(commit=False)
                blood_date.username = username
                blood_date.save()
                messages.success(request, '')
            
            # Проверяем источник запроса
            if request.POST.get('source') == 'profile':
                return redirect('profile')
            else:
                return redirect('schedule_donation')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
            return render(request, 'planirovanie.html', {'form': form})
    return redirect('planing_donor')
