from django import forms
from .models import Comment  # Импортируйте модель Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Укажите поля, которые должны отображаться в форме
