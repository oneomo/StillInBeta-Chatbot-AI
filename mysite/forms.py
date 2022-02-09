from django import forms
from django.forms import ModelForm
from django.forms.models import fields_for_model
from django.contrib.auth.forms import UserCreationForm, UserModel
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
