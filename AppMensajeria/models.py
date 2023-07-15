from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Mensaje(models.Model):
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuario: {self.usuario} - Contenido: {self.contenido}"
