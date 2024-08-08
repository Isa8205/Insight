from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from main.models import Articles, Users

class SignupForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['full_name', 'username','email', 'password1', 'password2', 'profile']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.full_name = self.cleaned_data["full_name"]
            user.profile = self.cleaned_data["profile"]
            if commit:
                user.save()
            return user
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=15, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['author', 'title', 'content']


