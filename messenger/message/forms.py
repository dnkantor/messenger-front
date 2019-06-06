from django import forms
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import requests

class SendMessageForm(forms.Form):
	message = forms.CharField()
	choicesList = list(User.objects.all().values_list('username', flat=True))
	CHOICES = []
	for value in choicesList:
		newTuple = (value, value);
		CHOICES.append(newTuple);

	receiver = forms.CharField(label="Who would you like to send it to?", widget=forms.Select(choices=CHOICES))