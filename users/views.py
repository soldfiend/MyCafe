from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.models import Group


# Create your views here.

def user(request):
    return render(request, 'users/test_user.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')  # Перенаправление на главную страницу после входа
        else:
            # Обработка неверных учетных данных
            error_message = "Invalid username or password."
            return render(request, 'users/login.html', {'error_message': error_message})
    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Получаем группу "Customer"
            group = Group.objects.get(name='Customer')

            # Добавляем пользователя в группу "Customer"
            group.user_set.add(user)

            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('user')

