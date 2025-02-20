from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # Para restringir acceso a vistas basadas en clases
from django.contrib.auth.decorators import login_required  # Para restringir acceso a vistas basadas en funciones
from .models import Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer

# Restringir acceso a la vista home
@login_required
def home(request):
    return render(request, 'blog/index.html', {'saludo': 'Hola, bienvenido'})

# Vista para listar posts (solo usuarios autenticados)
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    login_url = 'login'  # Redirige a la página de login si el usuario no está autenticado

# Vista para ver detalles de un post (solo usuarios autenticados)
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    login_url = 'login'

# Vista para crear un nuevo post (solo usuarios autenticados)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'contenido']
    login_url = 'login'

# Vista para actualizar un post (solo usuarios autenticados)
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'contenido']
    login_url = 'login'

# Vista para eliminar un post (solo usuarios autenticados)
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    login_url = 'login'

# APIViews para manejar las solicitudes HTTP
class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostDetail(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data)