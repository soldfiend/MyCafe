from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, get_object_or_404
from .models import Review
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from .models import Review


class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_context = []

        for review in context['reviews']:
            full_stars = range(review.rating)
            empty_stars = range(5 - review.rating)
            review_context.append({'review': review, 'full_stars': full_stars, 'empty_stars': empty_stars})

        context['reviews_context'] = review_context
        return context


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy('reviews_list')  # Замените 'reviews_list' на имя вашего URL-маршрута для списка отзывов
    template_name = 'review_list.html'  # Замените 'your_template_name.html' на имя вашего шаблона для удаления отзыва


def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews_list')
        else:
            # Вывести ошибки валидации в консоль для отладки
            print(form.errors)
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_list.html', {'form': form})
