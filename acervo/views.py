from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PecasAcervoForm
from .models import PecasAcervo


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


def peca_delete(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)

    if request.method == "POST":
        peca.delete()
        return redirect("pecas_acervo")

    return render(request, "pecas/peca_confirm_delete.html", {"peca": peca})


