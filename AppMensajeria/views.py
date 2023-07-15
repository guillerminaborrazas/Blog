from django.shortcuts import render, redirect
from .models import *
from AppGeneral.views import getavatar
from .forms import formNewMessage
# Create your views here.

def mensajes(request):
    avatar = getavatar(request)
    if request.method == "POST":
        form = formNewMessage(request.POST) # Aqui me llega la informacion del html
        if form.is_valid():
            usuario = User.objects.get(username = request.user)
            message = Mensaje(usuario = usuario, contenido = form.cleaned_data['contenido'])
            message.save()
            form = formNewMessage()
            todos = Mensaje.objects.all()
            return render(request, 'AppMensajeria/mensajeria.html', {'form': form, 'avatar': avatar, 'todos':todos})
    else: 
        form = formNewMessage()
        todos = Mensaje.objects.all()
        return render(request, 'AppMensajeria/mensajeria.html', {'form': form, 'avatar': avatar, 'todos':todos})