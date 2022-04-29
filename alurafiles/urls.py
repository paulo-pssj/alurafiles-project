from unicodedata import name

from django.urls import path

from alurafiles import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detalhes/<slug:date>', views.detalhes, name='detalhes'),
    path('analise/', views.analise, name='analise'),
    path(
        'analise_suspeitos/', views.analise_suspeitos, name='analise_suspeitos'
    ),
]
