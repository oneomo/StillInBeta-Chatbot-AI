from django.shortcuts import render, redirect 
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .decorators import unauthenticated_user
from django.contrib import messages
from .ChatBotAnswer import makeAnswer

def home(request):
    if request.method == "POST":
        answer = makeAnswer(request)
        return HttpResponse(str(answer))
    return render(request, 'mysite/home.html')

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Fiók létrehozva ' + username + ' számára')

			return redirect('login')
	context = {'form':form}
	return render(request, 'mysite/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'A felhasználónév vagy a jelszó nem megfelelő')

	context = {}
	return render(request, 'mysite/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')
