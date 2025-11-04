from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("memorial/", views.acervo_publico, name="acervo_publico"),
    path("memorial/peca/<int:pk>/", views.acervo_publico_peca, name="acervo_publico_peca"),
    path("pecas/", views.pecas_acervo, name="pecas_acervo"),
    path("pecas/adicionar/", views.peca_create, name="peca_create"),
    path("pecas/<int:pk>/editar/", views.peca_update, name="peca_update"),
    path("pecas/<int:pk>/excluir/", views.peca_delete, name="peca_delete"),
    path("pecas/<int:pk>/midias/", views.peca_midias, name="peca_midias"),
    path(
        "pecas/<int:peca_pk>/midias/<int:midia_pk>/excluir/",
        views.peca_midia_delete,
        name="peca_midia_delete",
    ),
    path(
        "pecas/<int:peca_pk>/historico/",
        views.peca_historico_list,
        name="peca_historico_list",
    ),
    path(
        "pecas/<int:peca_pk>/historico/adicionar/",
        views.peca_historico_create,
        name="peca_historico_create",
    ),
    path(
        "pecas/<int:peca_pk>/historico/<int:pk>/editar/",
        views.peca_historico_update,
        name="peca_historico_update",
    ),
    path(
        "pecas/<int:peca_pk>/historico/<int:pk>/excluir/",
        views.peca_historico_delete,
        name="peca_historico_delete",
    ),
    path("pessoas/", views.pessoas_list, name="pessoas_list"),
    path("pessoas/adicionar/", views.pessoa_create, name="pessoa_create"),
    path("pessoas/<int:pk>/editar/", views.pessoa_update, name="pessoa_update"),
    path("pessoas/<int:pk>/excluir/", views.pessoa_delete, name="pessoa_delete"),
    path("exposicoes/", views.exposicoes_list, name="exposicoes_list"),
    path("exposicoes/adicionar/", views.exposicao_create, name="exposicao_create"),
    path("exposicoes/<int:pk>/editar/", views.exposicao_update, name="exposicao_update"),
    path("exposicoes/<int:pk>/excluir/", views.exposicao_delete, name="exposicao_delete"),
    path("configuracoes/eixos/", views.eixos_list, name="eixos_list"),
    path("configuracoes/eixos/adicionar/", views.eixo_create, name="eixo_create"),
    path("configuracoes/eixos/<int:pk>/editar/", views.eixo_update, name="eixo_update"),
    path("configuracoes/eixos/<int:pk>/excluir/", views.eixo_delete, name="eixo_delete"),
    path("configuracoes/sistema/", views.configuracoes_sistema, name="config_sistema"),
    path("configuracoes/locais-internos/", views.locais_internos_list, name="locais_internos_list"),
    path("configuracoes/locais-internos/adicionar/", views.local_interno_create, name="local_interno_create"),
    path("configuracoes/locais-internos/<int:pk>/editar/", views.local_interno_update, name="local_interno_update"),
    path("configuracoes/locais-internos/<int:pk>/excluir/", views.local_interno_delete, name="local_interno_delete"),
    path("configuracoes/tipos-evento/", views.tipos_evento_list, name="tipos_evento_list"),
    path("configuracoes/tipos-evento/adicionar/", views.tipo_evento_create, name="tipo_evento_create"),
    path("configuracoes/tipos-evento/<int:pk>/editar/", views.tipo_evento_update, name="tipo_evento_update"),
    path("configuracoes/tipos-evento/<int:pk>/excluir/", views.tipo_evento_delete, name="tipo_evento_delete"),
]

