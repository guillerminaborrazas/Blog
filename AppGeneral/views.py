from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, UpdateView

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
    avatar = getavatar(request)
    return render(request, 'AppGeneral/perfil.html', {'user': user,'avatar': avatar})

@login_required  
def editProfile(request):
    avatar = getavatar(request)
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
        return render(request, 'AppGeneral/editarPerfil.html', {"form": form, 'avatar': avatar})

@login_required    
def crearNuevaPublicacion(request):
    if request.method == "POST":
        miFormulario = formSetBlog(request.POST, request.FILES) # Aqui me llega la informacion del html
        print(miFormulario)
        if miFormulario.is_valid():
            autor = User.objects.get(username = request.user)
            blog = Blog(autor = autor, imagen = miFormulario.cleaned_data['imagen'], pais = miFormulario.cleaned_data['pais'], titulo = miFormulario.cleaned_data['titulo'], subtitulo = miFormulario.cleaned_data['subtitulo'], cuerpo = miFormulario.cleaned_data['cuerpo'])
            blog.save()
            miFormulario = formSetBlog()
            #blogs = Blog.objects.get()
            #avatar = getavatar(request)
            return redirect('/pages/')
    else: 
        miFormulario = formSetBlog()
        avatar = getavatar(request)
        return render(request, "AppGeneral/setBlog.html", {'miFormulario': miFormulario, 'avatar': avatar})

@login_required
def cambiarPassword(request):
    avatar = getavatar(request)
    usuario = request.user    
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            if request.POST['new_password1'] == request.POST['new_password2']:
                user = form.save()
                update_session_auth_hash(request, user)
            #return render(request, 'AppGeneral/changePassword.html', {'error': 'Las contraseñas no coinciden'})
        return redirect('/profile/')
    else:
        form = ChangePasswordForm(user = usuario)
        return render(request, 'AppGeneral/changePassword.html', {"form": form, 'avatar': avatar})
@login_required   
def about(request):
    avatar = getavatar(request)
    return render(request, 'AppGeneral/about.html', {'avatar': avatar})

#class BlogView(ListView):
    #model = Blog

@login_required
def pages(request):
    avatar = getavatar(request)
    blogs = Blog.objects.get_queryset()
    return render(request, 'AppGeneral/pages.html', {'blogs': blogs, 'avatar': avatar})



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
    return render(request, "AppGeneral/avatar.html", {'form': form, 'avatar': avatar})

@login_required
def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar

@login_required
def eliminarBlog(request, id):
    blog = Blog.objects.get(id = id)
    blog.delete()
    return redirect ('/pages/')
    
@login_required
def editarBlog(request, id):
    blog = Blog.objects.get(id = id)
    if request.method == 'POST':
        miFormulario = formSetBlog(request.POST, request.FILES)
        if miFormulario.is_valid:
            print(miFormulario)
            data = miFormulario.cleaned_data

            blog.pais = data['pais']
            blog.titulo = data['titulo']
            blog.subtitulo = data['subtitulo']
            blog.cuerpo = data['cuerpo']
            try:
                blog.imagen = data['imagen']
            except:
                blog.imagen = blog.imagen
            blog.save()
            return redirect ('/pages/')
    else:
        miFormulario = formSetBlog(initial={'pais': blog.pais, 'titulo': blog.titulo, 'subtitulo': blog.subtitulo, 'cuerpo': blog.cuerpo, 'imagen': blog.imagen})
        avatar = getavatar(request)
        return render(request, "AppGeneral/editarBlog.html", {"miFormulario": miFormulario, 'avatar': avatar})

@login_required
def verBlog(request, id):
    blog = Blog.objects.get(id = id)
    avatar = getavatar(request)
    return render(request, 'AppGeneral/blog.html', {'blog': blog, 'avatar': avatar})

@login_required
def buscoBlog(request):
    avatar = getavatar(request)
    if request.method == 'POST':
        form = buscarBlog(request.POST)
        if form.is_valid():
            paisBuscado = form.cleaned_data['pais']
            blog = Blog.objects.filter(pais = paisBuscado)
            form = buscarBlog()
            return render(request, 'AppGeneral/busquedaBlog.html', {'blog':blog, 'avatar': avatar, 'form': form})
    else:
        blog = Blog.objects.get_queryset()
        form = buscarBlog()
        return render(request, 'AppGeneral/busquedaBlog.html', {'blog':blog, 'avatar': avatar, 'form': form})
