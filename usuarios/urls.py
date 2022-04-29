from django.urls import path

from usuarios import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('cadastrados', views.usuarios_cadastrados, name='cadastrados'),
    path('editar/<user_id>', views.editar_usuarios, name='editar_usuarios'),
    path(
        'atualiza_usuarios', views.atualiza_usuarios, name='atualiza_usuarios'
    ),
    path('deletar/<int:user_id>', views.deletar, name='deletar'),
]
