from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# Vista para listar todos los posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'  # Variable que se pasará a la plantilla

# Vista para ver los detalles de un post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

# Vista para crear un nuevo post
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'contenido']  # Campos que se mostrarán en el formulario

# Vista para actualizar un post existente
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['titulo', 'contenido']  # Campos que se podrán editar

# Vista para eliminar un post
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')  # Redirige a la lista de posts después de eliminar
