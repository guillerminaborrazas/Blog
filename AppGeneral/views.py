from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *

# Create your views here.
@login_required
def inicio(request):
    return(render(request, "AppGeneral/inicio.html"))

def loginWeb(request):
    if request.method == "POST":
        user = authenticate(username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("../")
        else:
            return render(request, 'AppGeneral/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'AppGeneral/login.html')

def registro(request):
    if request.method == "POST":
        userCreate = UserCreationForm(request.POST)
        if userCreate is not None:
            userCreate.save()
            return redirect("/login/")
        else:
            return render(request, 'AppGeneral/registro.html', {'error': 'El usuario no pudo ser creado'})
    else:
        return render(request, 'AppGeneral/registro.html')

@login_required  
def viewProfile(request):  
    return render(request, 'AppGeneral/perfil.html')

@login_required  
def editProfile(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'AppCoder/perfil.html')
    else:
        form = UserEditForm(initial= {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'AppCoder/editarPerfil.html', {"form": form})

def cambiarPassword(request):
    pass
def about(request):
    pass
def pages(request):
    pass
def mensajes(request):
    pass