from django.db import models
from django.core.validators import MaxValueValidator
import datetime

SITUACAO = {
    "LC": "Localizado",
    "NL": "Não localizado",
    "EX": "Excluído"
}

CONSERVACAO = {
    "BOM": "Bom",
    "RAZ": "Razoável",
    "RUI": "Ruim",
    "INT": "Inutilizada"
}

TIPOLOGIA = {
    "MUS": "Museológico",
    "BIB": "Bibliográfico",
    "ARQ": "Arquivístico"
}

AQUISICAO = {
    "DOA": "Doação",
    "CMP": "Compra",
    "EMP": "Empréstimo/Depósito",
    "LEG": "Legado",
    "PMT": "Permuta",
    "PRE": "Premiação",
    "TRF": "Transferência"
}

TIPO_MIDIA_DIGITAL = {
    "F": "Foto/Digitalização",
    "V": "Vídeo",
    "A": "Áudio"
}


def hoje():
    return datetime.date.today()


class Pessoa(models.Model):
    
    nome = models.CharField(max_length=100, null=False, blank=False)
    fones = models.CharField(max_length=40, null=True, blank=True)
    email= models.CharField(max_length=100, null=True, blank=True)
    naturalidade = models.CharField(max_length=40, null=True, blank=True)
    nacionalidade = models.CharField(max_length=20, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True, validators=[MaxValueValidator(limit_value=hoje)])
    biografia = models.TextField(null=True, blank=False)
    pessoa_fisica = models.BooleanField(default=True, null=False)
    autor_de_obra = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.nome


class EixoOrganizador(models.Model):
    
    eixo = models.CharField(max_length=100, null=False, blank=False)    

    def __str__(self):
        return self.eixo


class Exposicao(models.Model):
    
    nome = models.CharField(max_length=200, null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    data_inicio = models.DateField(null=False, blank=False)
    data_final = models.DateField(null=False, blank=False)
    local = models.CharField(max_length=255, null=False, blank=False)
    orgazador = models.CharField(max_length=200, null=False, blank=False)


class LocalInterno(models.Model):
    local = models.CharField(max_length=100, null=False, blank=False)    

    def __str__(self):
        return self.local
       

class PecasAcervo(models.Model):

    denominacao = models.CharField(max_length=100, null=False, blank=False)
    autor = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, )
    titulo_dado_pelo_autor = models.CharField(max_length=100, null=False, blank=False)
    nr_registro = models.CharField(max_length=10, null=True, blank=True)
    numero_ordem = models.CharField(max_length=3, null=True, blank=True)
    situacao = models.CharField(max_length=2, choices=SITUACAO, default="LC")
    thesaurus = models.CharField(max_length=100, null=True, blank=True)
    resumo_descritivo = models.TextField(null=False, blank=False)
    dimensoes = models.CharField(max_length=30, null=True, blank=True)
    material_tecnica = models.TextField(null=False, blank=False)
    estado_conservacao = models.CharField(max_length=3, choices=CONSERVACAO)
    local_producao = models.CharField(max_length=200, null=False, blank=False)
    data_inicial_producao = models.DateField(validators=[MaxValueValidator(limit_value=hoje)], null=True, blank=True)
    data_final_producao = models.DateField(validators=[MaxValueValidator(limit_value=hoje)], null=True, blank=True)
    pode_reproduzir = models.BooleanField(default=False, null=False)
    condicoes_reproducao = models.TextField(null=True, blank=True)
    tipologia = models.CharField(max_length=3, choices=TIPOLOGIA, default="MUS")
    eixo_organizador = models.ForeignKey(EixoOrganizador, null=True, blank=True, on_delete=models.SET_NULL)
    exposicao = models.ForeignKey(Exposicao, null=True, blank=True, on_delete=models.SET_NULL)
    forma_aquisicao = models.CharField(max_length=3, null=False, blank=False, choices=AQUISICAO)
    localizacao_interna = models.ForeignKey(LocalInterno, null=True, blank=True, on_delete=models.SET_NULL)
    publicada = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.denominacao
    

class Midia(models.Model):
    
    peca_acervo = models.ForeignKey(PecasAcervo, on_delete=models.CASCADE, null=False, blank=False)
    tipo = models.CharField(max_length=1, choices=TIPO_MIDIA_DIGITAL, default="F", blank=False, null=False)

    def __str__(self):
        return f"{self.tipo} da(o) {self.peca_acervo}"
    

    