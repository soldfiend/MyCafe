from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='my_profile'),
    path('change_password/', views.change_password, name='change_password'),
]
