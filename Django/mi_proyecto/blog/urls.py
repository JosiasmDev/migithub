from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostList, PostDetail

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),  # Página principal
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/nuevo/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/editar/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/eliminar/', PostDeleteView.as_view(), name='post_delete'),

    # Rutas de autenticación
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='post_list'), name='logout'),  # Redirige tras cerrar sesión

    # rutas para las vistas de la API
    path('api/posts/', PostList.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
