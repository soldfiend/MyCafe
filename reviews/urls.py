# reviews/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='reviews_list'),  # Список отзывов
    path('add/', views.add_review, name='add_review'),  # Добавление отзыва
    path('delete_review/<int:pk>/', views.ReviewDeleteView.as_view(), name='delete_review'),

]
