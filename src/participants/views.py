from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from game.forms import PlayerForm

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
        register_form = RegisterUserForm(request.POST)
        player_form = PlayerForm(request.POST)
        if all((register_form.is_valid(), player_form.is_valid())):
            user_created = register_form.save()
            player = player_form.save(commit=False)
            player.user = user_created
            player.save()

            print(register_form.changed_data)
            print(register_form.fields)

            username = register_form.clean().get('username')
            password = register_form.clean().get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration duccessful"))
            return redirect('game:index')
    
    else :
        register_form = RegisterUserForm()
        player_form = PlayerForm()

    return render(request, 'authenticate/register_user.html', {'register_form': register_form, 'player_form': player_form})