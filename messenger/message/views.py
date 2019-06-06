from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import json
from .forms import SendMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required
def home(request):
	if (request.COOKIES['x-auth-token'] is None):
		redirect('login')

	getMessages = requests.get('http://localhost:3000/api/messages')

	if (request.method == 'POST'):
		form = SendMessageForm(request.POST)
		if form.is_valid():
			message = form.cleaned_data.get('message')
			receiver = User.objects.get(username=form.cleaned_data.get('receiver'))

			print(receiver.email);

			receiverId = requests.get(f'http://localhost:3000/api/users/{receiver.email}')
			
			if (receiverId.status_code is not 200):
				messages.error(request, 'That receiver does does not exist')
				return redirect('message-home');
			
			receiverId = receiverId.json();

			data = { "message" : message,
					 "senderId" : "5cf143e4e239700a6ae500dd",
					 "receiverId" : receiverId['_id']
				    }

			r = requests.post('http://localhost:3000/api/messages', json=data)
			if (r.status_code == 200):
				messages.success(request, f'Message was sent successfully')
			else:
				messages.error(request, f'Message was not sent successfully')
			return redirect('message-home')
	else:
		form = SendMessageForm()

	context = {
		'sendForm' : form,
		'allMessages' : getMessages.json()
	}

	return render(request, 'message/home.html', context)
