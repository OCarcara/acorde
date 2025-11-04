from collections import defaultdict
import json

from django.contrib import messages
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    MidiaFormSet,
    PecasAcervoForm,
    PessoaForm,
    ExposicaoForm,
    EixoOrganizadorForm,
    LocalInternoForm,
    TipoEventoPecaForm,
    HistoricoPecaForm,
    ConfigsForm,
)
from .models import (
    PecasAcervo,
    Pessoa,
    Exposicao,
    EixoOrganizador,
    LocalInterno,
    TipoEventoPeca,
    HistoricoPecas,
    Midia,
    Configs,
)


def index(request):
    return render(request, "index.html")


def pecas_acervo(request):
    pecas = (
        PecasAcervo.objects.all()
        .prefetch_related("autor")
        .order_by("denominacao")
    )
    return render(request, "pecas/pecas_acervo.html", {"pecas": pecas})


def peca_create(request):
    if request.method == "POST":
        form = PecasAcervoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pecas_acervo")
    else:
        form = PecasAcervoForm()

    context = {
        "form": form,
        "form_action": reverse("peca_create"),
        "titulo_pagina": "Adicionar peça ao acervo",
        "submit_label": "Adicionar peça",
    }
    return render(request, "pecas/peca_form.html", context)


def peca_update(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    if request.method == "POST":
        form = PecasAcervoForm(request.POST, instance=peca)
        if form.is_valid():
            form.save()
            return redirect("pecas_acervo")
    else:
        form = PecasAcervoForm(instance=peca)

    context = {
        "form": form,
        "peca": peca,
        "form_action": reverse("peca_update", args=[pk]),
        "titulo_pagina": "Editar peça",
        "submit_label": "Salvar alterações",
    }
    return render(request, "pecas/peca_form.html", context)


def peca_midias(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    midia_formset = MidiaFormSet(
        request.POST or None,
        request.FILES or None,
        instance=peca,
        prefix="midia",
    )

    if request.method == "POST" and midia_formset.is_valid():
        midia_formset.save()
        messages.success(request, "Mídias atualizadas.")
        return redirect("peca_midias", pk=pk)

    context = {
        "peca": peca,
        "midia_formset": midia_formset,
        "midias_existentes": list(peca.midias.all()),
    }
    return render(request, "pecas/midia_pecas.html", context)


def peca_midia_delete(request, peca_pk, midia_pk):
    peca = get_object_or_404(PecasAcervo, pk=peca_pk)
    midia = get_object_or_404(Midia, pk=midia_pk, peca_acervo=peca)

    if request.method == "POST":
        midia.delete()
        messages.success(request, "Mídia removida com sucesso.")

    return redirect("peca_midias", pk=peca_pk)


def peca_delete(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    if request.method == "POST":
        peca.delete()
        return redirect("pecas_acervo")

    return render(request, "pecas/peca_confirm_delete.html", {"peca": peca})


def peca_historico_list(request, peca_pk):
    peca = get_object_or_404(PecasAcervo, pk=peca_pk)
    historicos = (
        HistoricoPecas.objects.filter(peca=peca)
        .select_related("tipo_evento", "responsavel")
        .order_by("-data_inicio", "-pk")
    )
    context = {
        "peca": peca,
        "historicos": historicos,
    }
    return render(request, "pecas/historico_peca_list.html", context)


def peca_historico_create(request, peca_pk):
    peca = get_object_or_404(PecasAcervo, pk=peca_pk)

    if request.method == "POST":
        form = HistoricoPecaForm(request.POST)
        if form.is_valid():
            historico = form.save(commit=False)
            historico.peca = peca
            historico.save()
            return redirect("peca_historico_list", peca_pk=peca.pk)
    else:
        form = HistoricoPecaForm()

    context = {
        "form": form,
        "peca": peca,
        "form_action": reverse("peca_historico_create", args=[peca.pk]),
        "titulo_pagina": "Adicionar historico",
        "submit_label": "Adicionar historico",
    }
    return render(request, "pecas/historico_peca_form.html", context)


def peca_historico_update(request, peca_pk, pk):
    peca = get_object_or_404(PecasAcervo, pk=peca_pk)
    historico = get_object_or_404(HistoricoPecas, pk=pk, peca=peca)

    if request.method == "POST":
        form = HistoricoPecaForm(request.POST, instance=historico)
        if form.is_valid():
            form.save()
            return redirect("peca_historico_list", peca_pk=peca.pk)
    else:
        form = HistoricoPecaForm(instance=historico)

    context = {
        "form": form,
        "peca": peca,
        "historico": historico,
        "form_action": reverse("peca_historico_update", args=[peca.pk, pk]),
        "titulo_pagina": "Editar histórico",
        "submit_label": "Salvar alteracoes",
    }
    return render(request, "pecas/historico_peca_form.html", context)


def peca_historico_delete(request, peca_pk, pk):
    peca = get_object_or_404(PecasAcervo, pk=peca_pk)
    historico = get_object_or_404(HistoricoPecas, pk=pk, peca=peca)

    if request.method == "POST":
        historico.delete()
        return redirect("peca_historico_list", peca_pk=peca.pk)

    context = {
        "peca": peca,
        "historico": historico,
    }
    return render(request, "pecas/historico_peca_confirm_delete.html", context)


def pessoas_list(request):
    pessoas = Pessoa.objects.all().order_by("nome")
    return render(request, "pessoas/pessoas.html", {"pessoas": pessoas})


def pessoa_create(request):
    if request.method == "POST":
        form = PessoaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pessoas_list")
    else:
        form = PessoaForm()

    context = {
        "form": form,
        "form_action": reverse("pessoa_create"),
        "titulo_pagina": "Adicionar pessoa",
        "submit_label": "Adicionar pessoa",
    }
    return render(request, "pessoas/pessoa_form.html", context)


def pessoa_update(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)

    if request.method == "POST":
        form = PessoaForm(request.POST, instance=pessoa)
        if form.is_valid():
            form.save()
            return redirect("pessoas_list")
    else:
        form = PessoaForm(instance=pessoa)

    context = {
        "form": form,
        "pessoa": pessoa,
        "form_action": reverse("pessoa_update", args=[pk]),
        "titulo_pagina": "Editar pessoa",
        "submit_label": "Salvar alterações",
    }
    return render(request, "pessoas/pessoa_form.html", context)


def pessoa_delete(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)

    if request.method == "POST":
        pessoa.delete()
        return redirect("pessoas_list")

    return render(request, "pessoas/pessoa_confirm_delete.html", {"pessoa": pessoa})


def eixos_list(request):
    eixos = EixoOrganizador.objects.all().order_by("eixo")
    return render(request, "configuracoes/eixos.html", {"eixos": eixos})


def eixo_create(request):
    if request.method == "POST":
        form = EixoOrganizadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("eixos_list")
    else:
        form = EixoOrganizadorForm()

    context = {
        "form": form,
        "form_action": reverse("eixo_create"),
        "titulo_pagina": "Adicionar eixo organizador",
        "submit_label": "Adicionar eixo",
    }
    return render(request, "configuracoes/eixo_form.html", context)


def eixo_update(request, pk):
    eixo = get_object_or_404(EixoOrganizador, pk=pk)

    if request.method == "POST":
        form = EixoOrganizadorForm(request.POST, instance=eixo)
        if form.is_valid():
            form.save()
            return redirect("eixos_list")
    else:
        form = EixoOrganizadorForm(instance=eixo)

    context = {
        "form": form,
        "eixo": eixo,
        "form_action": reverse("eixo_update", args=[pk]),
        "titulo_pagina": "Editar eixo organizador",
        "submit_label": "Salvar alterações",
    }
    return render(request, "configuracoes/eixo_form.html", context)


def eixo_delete(request, pk):
    eixo = get_object_or_404(EixoOrganizador, pk=pk)

    if request.method == "POST":
        eixo.delete()
        return redirect("eixos_list")

    return render(request, "configuracoes/eixo_confirm_delete.html", {"eixo": eixo})


def locais_internos_list(request):
    locais = LocalInterno.objects.all().order_by("local")
    return render(request, "configuracoes/locais_internos.html", {"locais": locais})


def local_interno_create(request):
    if request.method == "POST":
        form = LocalInternoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("locais_internos_list")
    else:
        form = LocalInternoForm()

    context = {
        "form": form,
        "form_action": reverse("local_interno_create"),
        "titulo_pagina": "Adicionar local interno",
        "submit_label": "Adicionar local",
    }
    return render(request, "configuracoes/local_interno_form.html", context)


def local_interno_update(request, pk):
    local_interno = get_object_or_404(LocalInterno, pk=pk)

    if request.method == "POST":
        form = LocalInternoForm(request.POST, instance=local_interno)
        if form.is_valid():
            form.save()
            return redirect("locais_internos_list")
    else:
        form = LocalInternoForm(instance=local_interno)

    context = {
        "form": form,
        "local_interno": local_interno,
        "form_action": reverse("local_interno_update", args=[pk]),
        "titulo_pagina": "Editar local interno",
        "submit_label": "Salvar alterações",
    }
    return render(request, "configuracoes/local_interno_form.html", context)


def local_interno_delete(request, pk):
    local_interno = get_object_or_404(LocalInterno, pk=pk)

    if request.method == "POST":
        local_interno.delete()
        return redirect("locais_internos_list")

    return render(
        request,
        "configuracoes/local_interno_confirm_delete.html",
        {"local_interno": local_interno},
    )


def tipos_evento_list(request):
    tipos_evento = TipoEventoPeca.objects.all().order_by("desc_evento")
    return render(request, "configuracoes/tipos_evento.html", {"tipos_evento": tipos_evento})


def tipo_evento_create(request):
    if request.method == "POST":
        form = TipoEventoPecaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tipos_evento_list")
    else:
        form = TipoEventoPecaForm()

    context = {
        "form": form,
        "form_action": reverse("tipo_evento_create"),
        "titulo_pagina": "Adicionar tipo de evento",
        "submit_label": "Adicionar tipo",
    }
    return render(request, "configuracoes/tipo_evento_form.html", context)


def tipo_evento_update(request, pk):
    tipo_evento = get_object_or_404(TipoEventoPeca, pk=pk)

    if request.method == "POST":
        form = TipoEventoPecaForm(request.POST, instance=tipo_evento)
        if form.is_valid():
            form.save()
            return redirect("tipos_evento_list")
    else:
        form = TipoEventoPecaForm(instance=tipo_evento)

    context = {
        "form": form,
        "tipo_evento": tipo_evento,
        "form_action": reverse("tipo_evento_update", args=[pk]),
        "titulo_pagina": "Editar tipo de evento",
        "submit_label": "Salvar alterações",
    }
    return render(request, "configuracoes/tipo_evento_form.html", context)


def tipo_evento_delete(request, pk):
    tipo_evento = get_object_or_404(TipoEventoPeca, pk=pk)

    if request.method == "POST":
        tipo_evento.delete()
        return redirect("tipos_evento_list")

    return render(
        request,
        "configuracoes/tipo_evento_confirm_delete.html",
        {"tipo_evento": tipo_evento},
    )


def configuracoes_sistema(request):
    configs, _created = Configs.objects.get_or_create(pk=1, defaults={"open_ia_key": ""})

    if request.method == "POST":
        form = ConfigsForm(request.POST, instance=configs)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações atualizadas.")
            return redirect("config_sistema")
    else:
        form = ConfigsForm(instance=configs)

    context = {
        "form": form,
        "form_action": reverse("config_sistema"),
        "titulo_pagina": "Configuracoes do sistema",
        "submit_label": "Salvar configuracoes",
    }
    return render(request, "configs/config_form.html", context)


def exposicoes_list(request):
    exposicoes = Exposicao.objects.all().order_by("-data_inicio")
    return render(request, "exposicoes/exposicoes.html", {"exposicoes": exposicoes})


def exposicao_create(request):
    if request.method == "POST":
        form = ExposicaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exposicoes_list")
    else:
        form = ExposicaoForm()

    context = {
        "form": form,
        "form_action": reverse("exposicao_create"),
        "titulo_pagina": "Adicionar exposição",
        "submit_label": "Adicionar exposição",
    }
    return render(request, "exposicoes/exposicao_form.html", context)


def exposicao_update(request, pk):
    exposicao = get_object_or_404(Exposicao, pk=pk)

    if request.method == "POST":
        form = ExposicaoForm(request.POST, instance=exposicao)
        if form.is_valid():
            form.save()
            return redirect("exposicoes_list")
    else:
        form = ExposicaoForm(instance=exposicao)

    context = {
        "form": form,
        "exposicao": exposicao,
        "form_action": reverse("exposicao_update", args=[pk]),
        "titulo_pagina": "Editar exposição",
        "submit_label": "Salvar alterações",
    }
    return render(request, "exposicoes/exposicao_form.html", context)


def exposicao_delete(request, pk):
    exposicao = get_object_or_404(Exposicao, pk=pk)

    if request.method == "POST":
        exposicao.delete()
        return redirect("exposicoes_list")

    return render(request, "exposicoes/exposicao_confirm_delete.html", {"exposicao": exposicao})



def acervo_publico(request):
    tipo = request.GET.get("tipo", "fisico")
    if tipo not in {"fisico", "digital"}:
        tipo = "fisico"

    exposicao_param = request.GET.get("exposicao", "").strip()
    exposicao_id = None
    if exposicao_param:
        try:
            exposicao_id = int(exposicao_param)
        except ValueError:
            exposicao_param = ""

    termo_busca = request.GET.get("q", "").strip()

    midias_prefetch = Prefetch("midias", queryset=Midia.objects.order_by("pk"))
    autores_prefetch = Prefetch("autor", queryset=Pessoa.objects.order_by("nome"))

    exposicoes_por_tipo_qs = {
        "fisico": Exposicao.objects.filter(exposicao_fisica=True).order_by("nome"),
        "digital": Exposicao.objects.filter(exposicao_fisica=False).order_by("nome"),
    }

    exposicoes_para_select = list(exposicoes_por_tipo_qs[tipo])
    exposicoes_por_tipo_json = json.dumps(
        {
            chave: [{"id": str(expo.pk), "nome": expo.nome} for expo in qs]
            for chave, qs in exposicoes_por_tipo_qs.items()
        },
        ensure_ascii=False,
    )

    pecas_base = (
        PecasAcervo.objects.filter(publicada=True)
        .select_related("eixo_organizador", "localizacao_interna", "exposicao")
        .prefetch_related(autores_prefetch, midias_prefetch)
        .order_by("denominacao")
    )

    if tipo == "fisico":
        pecas_base = pecas_base.filter(exposicao__exposicao_fisica=True)
    elif tipo == "digital":
        pecas_base = pecas_base.filter(exposicao__exposicao_fisica=False)

    if exposicao_id is not None:
        pecas_base = pecas_base.filter(exposicao__pk=exposicao_id)

    resultados = []
    grupos = []

    if termo_busca:
        resultados = list(
            pecas_base.filter(
                Q(denominacao__icontains=termo_busca)
                | Q(autor__nome__icontains=termo_busca)
            )
            .distinct()
            .order_by("denominacao")
        )
    else:
        pecas_list = list(pecas_base)
        if tipo == "fisico":
            agrupador = defaultdict(list)
            for peca in pecas_list:
                chave = (
                    peca.eixo_organizador.eixo
                    if peca.eixo_organizador
                    else "Eixo não informado"
                )
                agrupador[chave].append(peca)

            grupos = [
                {
                    "titulo": chave,
                    "pecas": sorted(itens, key=lambda p: p.denominacao),
                }
                for chave, itens in sorted(agrupador.items(), key=lambda item: item[0])
            ]
        else:
            resultados = sorted(pecas_list, key=lambda p: p.denominacao)

    context = {
        "tipo": tipo,
        "busca": termo_busca,
        "grupos": grupos,
        "resultados": resultados,
        "mostrando_busca": bool(termo_busca),
        "exposicoes": exposicoes_para_select,
        "exposicoes_por_tipo_json": exposicoes_por_tipo_json,
        "exposicao_param": exposicao_param,
    }
    return render(request, "acervo_publico/acervo_publico.html", context)


def acervo_publico_peca(request, pk):
    midias_prefetch = Prefetch("midias", queryset=Midia.objects.order_by("pk"))
    autores_prefetch = Prefetch("autor", queryset=Pessoa.objects.order_by("nome"))

    peca = get_object_or_404(
        PecasAcervo.objects.filter(publicada=True)
        .select_related(
            "eixo_organizador",
            "exposicao",
            "localizacao_interna",
        )
        .prefetch_related(autores_prefetch, midias_prefetch),
        pk=pk,
    )

    context = {
        "peca": peca,
        "midias": list(peca.midias.all()),
        "autores": list(peca.autor.all()),
    }
    return render(request, "acervo_publico/peca_detalhe.html", context)
