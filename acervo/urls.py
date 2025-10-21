from django.urls import path
from . import views

urlpatterns = [
    path("pecas", views.pecas_acervo),
    path("", views.index, name="index"),
    path("pecas/", views.pecas_acervo, name="pecas_acervo"),
    path("pecas/add/", views.peca_create, name="pecas_add"),
    path("pecas/<int:pk>/edit/", views.peca_update, name="pecas_edit"),
    path("pecas/<int:pk>/delete/", views.peca_delete, name="pecas_delete"),
]

