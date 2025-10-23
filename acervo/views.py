from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import PecasAcervo, Midia


def index(request):
    return render(request, "index.html")


def pecas_acervo(request):
    pecas = PecasAcervo.objects.all().order_by("denominacao")
    return render(request, "pecas/pecas_acervo.html", {"pecas": pecas})

def editar_peca(request, pk):
    peca = PecasAcervo.objects.get(id=pk)
    if peca:
        return render(request, "pecas/peca_form.html", {'peca': peca})
    pecas_acervo()

def atualizar_peca(request, pk):
    pecas_acervo()


