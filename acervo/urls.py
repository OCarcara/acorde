from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pecas/", views.pecas_acervo, name="pecas_acervo"),
    path("pecas/adicionar/", views.peca_create, name="peca_create"),
    path("pecas/<int:pk>/editar/", views.peca_update, name="peca_update"),
    path("pecas/<int:pk>/excluir/", views.peca_delete, name="peca_delete"),
    path("pessoas/", views.pessoas_list, name="pessoas_list"),
    path("pessoas/adicionar/", views.pessoa_create, name="pessoa_create"),
    path("pessoas/<int:pk>/editar/", views.pessoa_update, name="pessoa_update"),
    path("pessoas/<int:pk>/excluir/", views.pessoa_delete, name="pessoa_delete"),
    path("exposicoes/", views.exposicoes_list, name="exposicoes_list"),
    path("exposicoes/adicionar/", views.exposicao_create, name="exposicao_create"),
    path("exposicoes/<int:pk>/editar/", views.exposicao_update, name="exposicao_update"),
    path("exposicoes/<int:pk>/excluir/", views.exposicao_delete, name="exposicao_delete"),
]

