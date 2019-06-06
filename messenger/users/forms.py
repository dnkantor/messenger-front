from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=255)
	password = forms.CharField(widget=forms.PasswordInput())