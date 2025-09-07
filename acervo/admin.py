from django.contrib import admin
from .models import Pessoa, EixoOrganizador, Exposicao, LocalInterno, PecasAcervo, Midia


class PessoaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Pessoa, PessoaAdmin)


class EixoOrganizadorAdmin(admin.ModelAdmin):
    pass
admin.site.register(EixoOrganizador, EixoOrganizadorAdmin)


class ExposicaoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Exposicao, ExposicaoAdmin)


class LocalInternoAdmin(admin.ModelAdmin):
    pass
admin.site.register(LocalInterno, LocalInternoAdmin)


class PecasAcervoAdmin(admin.ModelAdmin):
    pass
admin.site.register(PecasAcervo, PecasAcervoAdmin)


class MidiaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Midia, MidiaAdmin)
