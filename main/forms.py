from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from main.models import Articles, Users

class SignupForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['full_name', 'username','email', 'password', 'profile']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['author', 'title', 'content']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)