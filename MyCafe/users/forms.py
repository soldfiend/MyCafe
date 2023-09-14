from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        # Здесь мы добавляем чат ID из формы, если он был отправлен
        if 'telegram_chat_id' in self.cleaned_data:
            user.telegram_chat_id = self.cleaned_data['telegram_chat_id']

        if commit:
            user.save()
        return user
