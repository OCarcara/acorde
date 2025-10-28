from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MidiaFormSet, PecasAcervoForm, PessoaForm
from .models import PecasAcervo, Pessoa


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


