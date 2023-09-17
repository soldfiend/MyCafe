from django import forms
from .models import HomePagePhoto


class HomePagePhotoForm(forms.ModelForm):
    class Meta:
        model = HomePagePhoto
        fields = ['image']
