from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import requests
from .forms import UserRegisterForm, LoginForm

# Create your views here.

def register(request):
	##Validate it 
	if (request.method == 'POST'):
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password1')

			data = { "name" : username,
					 "email" : email,
					 "password" : password
				    }
			r = requests.post('http://localhost:3000/api/users', json=data)
			if (r.status_code == 200):
				messages.success(request, f'User was created successfully')
				resp = redirect('login')
				resp.set_cookie('x-auth-token', value= r.headers['x-auth-token'])
				return resp
			else:
				messages.error(request, f'User was not created successfully')
	else:
		form = UserRegisterForm()

	return render(request, 'users/register.html', {'form': form})


def loginUser(request):
	if (request.method == 'POST'):
		#Post logic here
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username, password=password);

			if user is None:
				messages.error(request, f'Error: No such user.')
				return redirect('login');

			data = {
				"email": user.email,
				"password": password
			}

			r = requests.post('http://localhost:3000/api/auth', json=data)
			if (r.status_code == 200):
				login(request, user);
				messages.success(request, f'Successfully logged in.')
				resp = redirect('message-home')
				resp.set_cookie('x-auth-token', value= r.headers['x-auth-token'])
				return resp
			else:
				messages.error(request, f'Error: Could not log in.')
				redirect('login');
	else:
		form = LoginForm()

	return render(request, 'users/login.html', {'form': form })

def logoutUser(request):
	logout(request);
	resp = redirect('login');
	resp.delete_cookie('x-auth-token')
	messages.success(request, f'Successfully logged out.')
	return resp;

