from django.contrib import admin
from django.urls import path
from AppGeneral.views import *
from django.contrib.auth.views import LogoutView
from AppMensajeria.views import mensajes

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
    path('pages/<id>', verBlog, name='blog_ver'),
    path('editBlog/<id>', editarBlog, name='blog_editar'),
    path('deleteBlog/<id>', eliminarBlog, name='blog_eliminar'),
    path('editAvatar/', editAvatar, name='Avatar'),
    path('findBlog/', buscoBlog, name='buscarBlog'),
    path('logout', LogoutView.as_view(template_name= 'AppGeneral/login.html'), name = 'Logout'),
    
]