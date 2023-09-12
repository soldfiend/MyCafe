from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def profile(request):
    user = request.user  # Получаем текущего пользователя
    # Здесь вы можете получить информацию о пользователе и передать ее в контекст
    context = {
        'user': user,
    }
    return render(request, 'profile/main_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Обновление сессии после изменения пароля
            messages.success(request, 'Ваш пароль успешно изменен.')
            return redirect('my_profile')  # Перенаправление на страницу профиля после изменения пароля
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profile/change_password.html', {'form': form})
