from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("pecas/", views.pecas_acervo, name="pecas_acervo"),
    path("pecas/<int:pk>/edit/", views.editar_peca, name="editar_peca"),
    path("pecas/<int:pk>/atualizar/", views.atualizar_peca, name="atualizar_peca"),
]
"""     path("pecas/add/", views.peca_create, name="pecas_add"),
    path("pecas/<int:pk>/delete/", views.peca_delete, name="pecas_delete"), """

