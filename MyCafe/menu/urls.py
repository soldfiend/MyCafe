from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('add_dish/', views.add_dish, name='add_dish'),
    path('<int:pk>/update/', views.DishUpdateView.as_view(), name='change_dish'),
    path('<int:pk>/', views.DishDetailView.as_view(), name='dish_detail'),
    path('<int:pk>/delete', views.DishDeleteView.as_view(), name='dish_delete'),
]
