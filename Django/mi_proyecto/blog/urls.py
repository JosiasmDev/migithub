from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/nuevo/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/editar/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/eliminar/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Rutas de autenticación
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirige tras cerrar sesión
]
