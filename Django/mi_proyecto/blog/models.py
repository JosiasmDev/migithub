from django.db import models
from django.urls import reverse

class Post(models.Model):
    titulo = models.CharField(max_length=200)  # Título del post
    contenido = models.TextField()  # Contenido del post
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación, se asigna automáticamente

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
from django.db import models

# Create your models here.
