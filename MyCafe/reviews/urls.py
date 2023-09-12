# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews'  # Добавьте это, чтобы использовать пространство имен

urlpatterns = [
    path('add_review/', views.add_review, name='add_review'),

    # Пример URL-шаблона
    # Другие URL-шаблоны вашего приложения
]
