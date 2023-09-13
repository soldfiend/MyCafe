from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'telegram_chat_id']
