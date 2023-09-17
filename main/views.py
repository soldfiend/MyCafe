from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import HomePagePhotoForm
from .models import HomePagePhoto
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import HomePagePhoto
from django.shortcuts import render, redirect
from django.core.mail import send_mail

# Create your views here.


import smtplib
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from django.contrib import messages


def send_email(message):
    sender = "my_cafe_step@rambler.ru"
    password = "Qwertyu12345"
    recipient = "my_cafe_step@rambler.ru"  # Замените на адрес получателя

    try:
        server = smtplib.SMTP_SSL("smtp.rambler.ru", 465)
        server.login(sender, password)

        msg = MIMEText(message)
        msg["Subject"] = "Contact Form Submission"
        msg["From"] = sender
        msg["To"] = recipient

        server.sendmail(sender, recipient, msg.as_string())

        server.quit()
        return True
    except Exception as ex:
        return str(ex)


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Отправка сообщения по электронной почте
        result = send_email(f'Имя: {name}\nEmail: {email}\nСообщение: {message}')

        if result is True:
            messages.success(request, 'Сообщение успешно отправлено!')
        else:
            messages.error(request, f'Ошибка при отправке сообщения: {result}')

        return redirect('contact')  # Перенаправление на страницу с подтверждением

    return render(request, 'contact.html')


def upload_home_page_photo(request):
    if request.user.groups.filter(name='Administration').exists():
        if request.method == 'POST':
            # Обработка POST-запроса для загрузки фотографий\

            form = HomePagePhotoForm(request.POST, request.FILES)
            if form.is_valid():
                # Обработка формы и сохранение фотографии
                form.save()
                # Очистка формы или выполнение других действий
    else:
        return HttpResponseForbidden("Доступ запрещен, вы не являетесь администратором.")
        # Получите список фотографий для отображения
    photos = HomePagePhoto.objects.all()

    context = {
        'form': HomePagePhotoForm(),  # Замените на вашу форму
        'photos': photos,  # Передайте список фотографий в контекст
    }

    return render(request, 'main/upload_home_page_photo.html', context)


@login_required
def delete_photo(request, photo_id):
    try:
        photo = HomePagePhoto.objects.get(pk=photo_id)
        # Добавьте проверку, что текущий пользователь имеет право удалять фотографии
        if request.user.groups.filter(name='Administration').exists():
            photo.delete()
            return redirect('upload_home_page_photo')
        else:
            return HttpResponseForbidden("Доступ запрещен, вы не являетесь администратором.")
    except HomePagePhoto.DoesNotExist:
        return HttpResponseNotFound("Фотография не найдена.")


def index(request):
    # Получите все объекты изображений
    home_page_photos = HomePagePhoto.objects.all()

    # Передайте их в контекст шаблона
    context = {'home_page_photos': home_page_photos}
    return render(request, 'main/layout.html', context)


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')
