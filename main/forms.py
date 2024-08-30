import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from main.models import Articles, Users

class SignupForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['firstname', 'lastname', 'username', 'email', 'phone_number', 'date_of_birth', 'password1', 'password2', 'profile']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile = self.cleaned_data["profile"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        if commit:
            user.save()
        return user
    
    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Define the pattern for invalid characters (allow letters, numbers, underscores, and dashes)
        if not re.match(r'^[\w-]+$', username):
            raise forms.ValidationError("Username contains invalid characters. Only letters, numbers, underscores, and dashes are allowed.")
        
        return username

        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content', 'cover_image']


