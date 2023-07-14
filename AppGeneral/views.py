from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.http import HttpResponse

# Create your views here.
@login_required
def inicio(request):
    avatar = getavatar(request)
    return(render(request, "AppGeneral/inicio.html", {"avatar": avatar}))

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
    user = request.user
    return render(request, 'AppGeneral/perfil.html', {'user': user})

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
            return render(request, 'AppGeneral/perfil.html')
    else:
        form = UserEditForm(initial= {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'AppGeneral/editarPerfil.html', {"form": form})

@login_required    
def crearNuevaPublicacion(request):
    if request.method == "POST":
        miFormulario = formSetBlog(request.POST) # Aqui me llega la informacion del html
        if miFormulario.is_valid():
            autor = User.objects.get(username = request.user)
            blog = Blog(autor = autor, imagen = miFormulario.cleaned_data['imagen'], titulo = miFormulario.cleaned_data['titulo'], subtitulo = miFormulario.cleaned_data['subtitulo'], cuerpo = miFormulario.cleaned_data['cuerpo'])
            blog.save()
            miFormulario = formSetBlog()
            return render(request, "AppGeneral/setBlog.html", {'miFormulario': miFormulario})
    else: 
        miFormulario = formSetBlog()
        return render(request, "AppGeneral/setBlog.html", {'miFormulario': miFormulario})

@login_required
def cambiarPassword(request):
    usuario = request.user    
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            if request.POST['new_password1'] == request.POST['new_password2']:
                user = form.save()
                update_session_auth_hash(request, user)
            return render(request, 'AppGeneral/changePassword.html', {'error': 'Las contraseñas no coinciden'})
        return redirect("/perfil/")
    else:
        form = ChangePasswordForm(user = usuario)
        return render(request, 'AppGeneral/changePassword.html', {"form": form})
@login_required   
def about(request):
    return render(request, 'AppGeneral/about.html')

@login_required
def pages(request):
    blogs = Blog.objects.get()
    return render(request, 'AppGeneral/pages.html', {'blogs': blogs})
def mensajes(request):
    pass

@login_required
def editAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None           
            return render(request, "AppGeneral/inicio.html", {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, "AppGeneral/avatar.html", {'form': form})

@login_required
def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar