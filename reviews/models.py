from django.db import models
from django.contrib.auth.models import User  # или CustomUser, если вы используете пользовательскую модель пользователя
from menu.models import Dish  # Импортируем модель блюда из вашего приложения "menu"
from django.conf import settings


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Пользователь, оставивший отзыв
    dish = models.ForeignKey('menu.Dish', on_delete=models.CASCADE, null=True)
    text = models.TextField()  # Текст отзыва
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Рейтинг от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания отзыва

    def __str__(self):
        return f'Review by {self.user.username} for {self.dish.name}'
