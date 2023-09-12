from .forms import DishForm
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish


# Create your views here.
class DishUpdateView(UpdateView):
    model = Dish
    template_name = 'menu/add_dish.html'
    form_class = DishForm
    success_url = '/menu'

    def get_initial(self):
        initial = super().get_initial()
        dish = self.get_object()  # Получаем существующее блюдо
        initial['name'] = dish.name
        initial['description'] = dish.description
        initial['price'] = dish.price
        # Добавьте другие поля, если необходимо
        return initial


class DishDeleteView(DeleteView):
    model = Dish
    success_url = '/menu/'
    template_name = 'menu/dish_delete.html'


class DishDetailView(DetailView):
    model = Dish
    template_name = 'menu/detail_dish.html'
    context_object_name = 'dish'


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Administration').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Доступ запрещен,вы не входите в группу Админитраторы")

    return _wrapped_view


@admin_required
def add_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = DishForm()
    return render(request, 'menu/add_dish.html', {'form': form})


def menu(request):
    # Получаем блюда из базы данных и сортируем их по категории
    dishes = Dish.objects.all().order_by('category')

    # Создаем словарь для хранения блюд по категориям
    menu_items = {
        'breakfast_items': [],
        'lunch_items': [],
        'dinner_items': [],
    }

    # Разделяем блюда по категориям
    for dish in dishes:
        if dish.category == 'breakfast':
            menu_items['breakfast_items'].append(dish)
        elif dish.category == 'lunch':
            menu_items['lunch_items'].append(dish)
        elif dish.category == 'dinner':
            menu_items['dinner_items'].append(dish)

    return render(request, 'menu/menu.html', menu_items)



