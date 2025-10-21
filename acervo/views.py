from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.forms import modelform_factory
from django.forms.models import inlineformset_factory

from .models import PecasAcervo, Midia


def index(request):
    return render(request, "index.html")


def pecas_acervo(request):
    pecas = PecasAcervo.objects.all().order_by("denominacao")
    return render(request, "pecas_acervo.html", {"pecas": pecas})


# Forms
PecaForm = modelform_factory(PecasAcervo, exclude=[])  # include all fields by default
MidiaFormSet = inlineformset_factory(PecasAcervo, Midia, fields=("tipo", "url_midia", "legenda"), extra=1, can_delete=True)


def peca_create(request):
    if request.method == "POST":
        form = PecaForm(request.POST)
        if form.is_valid():
            peca = form.save()
            formset = MidiaFormSet(request.POST, request.FILES, instance=peca)
            if formset.is_valid():
                formset.save()
                return redirect(reverse("pecas_acervo"))
        else:
            formset = MidiaFormSet(request.POST, request.FILES)
    else:
        form = PecaForm()
        formset = MidiaFormSet()

    return render(request, "peca_form.html", {"form": form, "formset": formset})


def peca_update(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)
    if request.method == "POST":
        form = PecaForm(request.POST, instance=peca)
        formset = MidiaFormSet(request.POST, request.FILES, instance=peca)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect(reverse("pecas_acervo"))
    else:
        form = PecaForm(instance=peca)
        formset = MidiaFormSet(instance=peca)

    return render(request, "peca_form.html", {"form": form, "formset": formset, "peca": peca})


def peca_delete(request, pk):
    peca = get_object_or_404(PecasAcervo, pk=pk)
    if request.method == "POST":
        peca.delete()
        return redirect(reverse("pecas_acervo"))
    return render(request, "peca_confirm_delete.html", {"peca": peca})

