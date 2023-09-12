from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('increase_cart_item/<int:cart_item_id>/', views.increase_cart_item, name='increase_cart_item'),
    path('decrease_cart_item/<int:cart_item_id>/', views.decrease_cart_item, name='decrease_cart_item'),

]
