from django.shortcuts import render, redirect
from .models import Review
from menu.models import Dish


# Create your views here.
# reviews/views.py


def add_review(request):
    if request.method == 'POST':
        # Получаем данные из формы
        review_text = request.POST['review_text']
        dish_id = request.POST['dish_id']  # Получаем ID блюда из скрытого поля

        # Создаем новый отзыв и сохраняем его в базе данных
        dish = Dish.objects.get(pk=dish_id)
        user = request.user  # Пользователь, оставляющий отзыв, предполагается, что пользователь авторизован
        review = Review.objects.create(dish=dish, user=user, text=review_text)

        # Перенаправляем пользователя обратно на страницу блюда
        return redirect('menu:dish_detail', pk=dish_id)



    # В случае GET-запроса (например, если кто-то попытается зайти по URL)
    # перенаправляем пользователя на главную страницу или другую нужную вам страницу.
    return redirect('menu:index')  # Измените на свой URL
