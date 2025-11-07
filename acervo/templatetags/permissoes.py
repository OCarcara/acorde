from django import template

from ..utils import usuario_pode_acessar_configuracoes

register = template.Library()


@register.filter(name="pode_ver_configuracoes")
def pode_ver_configuracoes(user):
    return usuario_pode_acessar_configuracoes(user)

