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
)
from .models import (
    PecasAcervo,
    Pessoa,
    Exposicao,
    EixoOrganizador,
    LocalInterno,
    TipoEventoPeca,
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
    empty_instance = PecasAcervo()

    if request.method == "POST":
        form = PecasAcervoForm(request.POST)
        midia_formset = MidiaFormSet(
            request.POST,
            request.FILES,
            instance=empty_instance,
            prefix="midia",
        )
        if form.is_valid() and midia_formset.is_valid():
            peca = form.save()
            midia_formset.instance = peca
            midia_formset.save()
            return redirect("pecas_acervo")
    else:
        form = PecasAcervoForm()
        midia_formset = MidiaFormSet(instance=empty_instance, prefix="midia")

    context = {
        "form": form,
        "midia_formset": midia_formset,
        "form_action": reverse("peca_create"),
        "titulo_pagina": "Adicionar peça ao acervo",
        "submit_label": "Adicionar peça",
    }
    return render(request, "pecas/peca_form.html", context)


def peca_update(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    if request.method == "POST":
        form = PecasAcervoForm(request.POST, instance=peca)
        midia_formset = MidiaFormSet(
            request.POST,
            request.FILES,
            instance=peca,
            prefix="midia",
        )
        if form.is_valid() and midia_formset.is_valid():
            form.save()
            midia_formset.save()
            return redirect("pecas_acervo")
    else:
        form = PecasAcervoForm(instance=peca)
        midia_formset = MidiaFormSet(instance=peca, prefix="midia")

    context = {
        "form": form,
        "midia_formset": midia_formset,
        "peca": peca,
        "form_action": reverse("peca_update", args=[pk]),
        "titulo_pagina": "Editar peça",
        "submit_label": "Salvar alterações",
    }
    return render(request, "pecas/peca_form.html", context)


def peca_delete(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    if request.method == "POST":
        peca.delete()
        return redirect("pecas_acervo")

    return render(request, "pecas/peca_confirm_delete.html", {"peca": peca})


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
