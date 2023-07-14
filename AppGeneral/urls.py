from django.contrib import admin
from django.urls import path
from AppGeneral.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', inicio, name="Inicio"),
    path('login/', loginWeb, name="Login"),
    path('register/', registro, name="Registro"),
    path('profile/', viewProfile, name='Perfil'),
    path('about/', about, name='About'), 
    path('pages/', pages, name='Pages'),
    path('messages/', mensajes, name= 'Mensajes'),
    path('cambioPassword/', cambiarPassword, name= 'cambioContrasena'),
    path('editProfile/', editProfile, name='EditarPerfil'),
    path('blogging/', crearNuevaPublicacion, name='Publicar'),
    path('logout', LogoutView.as_view(template_name= 'AppGeneral/login.html'), name = 'Logout'),
    
]