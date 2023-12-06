from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class PostCategoryForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'price', 'contact', 'image']