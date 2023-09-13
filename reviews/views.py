from django.shortcuts import render, redirect
from .models import Review
from menu.models import Dish


# Create your views here.
# reviews/views.py


from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish
from .forms import CommentForm  # Импортируйте форму для комментариев

def add_comment(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.dish = dish
            comment.user = request.user
            comment.save()
            return redirect('menu:dish_detail', pk=pk)

    return redirect('menu:index')  # Измените на свой URL

