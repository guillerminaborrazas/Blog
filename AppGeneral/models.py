from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):

    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    cuerpo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True, null = True, blank = True)
    imagen = models.ImageField(null=True, blank=True, upload_to="imagenes")
    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Titulo: {self.titulo} - Subtitulo: {self.subtitulo} - Autor: {self.autor}"

class Avatar(models.Model):
    #vinculo con el usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #SubCarpeta de avatares
    image = models.ImageField(upload_to='avatares', null = True, blank = True)
    
