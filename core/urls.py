# core/urls.py
from django.urls import path
from . import views 

app_name = "core" 

urlpatterns = [
    # HOME
    path("", views.home, name="home"), 

    path("registro/", views.registro_piloto_view, name="registro"),
    
    # --- CRUD de EQUIPE (JÁ EXISTE) ---
    path("equipes/", views.EquipeListView.as_view(), name="equipe_list"),
    path("equipes/nova/", views.EquipeCreateView.as_view(), name="equipe_create"),
    path("equipes/<int:pk>/editar/", views.EquipeUpdateView.as_view(), name="equipe_update"),
    path("equipes/<int:pk>/excluir/", views.EquipeDeleteView.as_view(), name="equipe_delete"),

    # --- CRUD de CARRO ---
    path("carros/", views.CarroListView.as_view(), name="carro_list"),
    path("carros/novo/", views.CarroCreateView.as_view(), name="carro_create"),
    path("carros/<int:pk>/editar/", views.CarroUpdateView.as_view(), name="carro_update"),
    path("carros/<int:pk>/excluir/", views.CarroDeleteView.as_view(), name="carro_delete"),
    
    # --- CRUD de PISTA ---
    path("pistas/", views.PistaListView.as_view(), name="pista_list"),
    path("pistas/nova/", views.PistaCreateView.as_view(), name="pista_create"),
    path("pistas/<int:pk>/editar/", views.PistaUpdateView.as_view(), name="pista_update"),
    path("pistas/<int:pk>/excluir/", views.PistaDeleteView.as_view(), name="pista_delete"),
    
    # --- CRUD de CORRIDA ---
    path("corridas/", views.CorridaListView.as_view(), name="corrida_list"),
    path("corridas/nova/", views.CorridaCreateView.as_view(), name="corrida_create"),
    path("corridas/<int:pk>/", views.CorridaDetailView.as_view(), name="corrida_detail"),
    path("corridas/<int:pk>/editar/", views.CorridaUpdateView.as_view(), name="corrida_update"),
    path("corridas/<int:pk>/excluir/", views.CorridaDeleteView.as_view(), name="corrida_delete"),
    
    # --- INSCRIÇÃO (Create View) ---
    # A inscrição é feita a partir do detalhe da Corrida, por isso o PK da Corrida vem primeiro
    path(
        "corridas/<int:corrida_pk>/inscrever/",
        views.InscricaoCreateView.as_view(),
        name="inscricao_create"
    ),
]