from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
import datetime

def register_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            year = int(request.POST.get('year'))
            month = int(request.POST.get('month'))
            day = int(request.POST.get('day'))

            birthday = datetime.date(year, month, day)
        except Exception:
            messages.error(request, 'Invalid birthday')

            return redirect('accounts:register')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.error(request, 'Email or username already in use')

            return redirect('accounts:register')

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            birthday=birthday
        )
        user.save()

        user = authenticate(request, username=email, password=password)
        login(request, user)

        return redirect('blog:home')

    return render(request, 'accounts/register.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            return redirect('blog:home')
        else:
            messages.error(request, 'Invalid username or password')

            return redirect('accounts:login')

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)

    return redirect('accounts:login')
