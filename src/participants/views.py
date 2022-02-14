from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request) :
    if request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('game:index')
        else :
            messages.success(request, ('Une erreur à eue lieu pour la connexion, réessaye :)'))
            return redirect('login')
    else :
        return render(request, 'authenticate/login.html', {})

def logout_user(request) :
    logout(request)
    return redirect('game:index')

def register_user(request) :
    if request.method == "POST" :
        form = RegisterUserForm(request.POST)
        if form.is_valid() :
            form.save()
            username = form.changed_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration duccessful"))
            return redirect('game:index')
    
    else :
        form = RegisterUserForm()

    return render(request, 'authenticate/register_user.html', {'form': form})