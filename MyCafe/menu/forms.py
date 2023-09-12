from django import forms
from .models import Dish, CATEGORY_CHOICES


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image_url', 'category']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'image_url': 'Ссылка на изображение',
            'category': 'Категория',
        }

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control-dish'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control-dish', 'style': 'height: 13vh;'}))
    image_url = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control-dish', 'style': 'height: 5vh;'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control-dish', 'style': 'height: 3vh;'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control-dish', 'style': 'height: 3vh;'}))
