from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pecas/", views.pecas_acervo, name="pecas_acervo"),
    path("pecas/adicionar/", views.peca_create, name="peca_create"),
    path("pecas/<int:pk>/editar/", views.peca_update, name="peca_update"),
    path("pecas/<int:pk>/excluir/", views.peca_delete, name="peca_delete"),
]

