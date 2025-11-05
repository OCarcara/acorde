from django.db import models
from django.core.files.uploadedfile import UploadedFile
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils.dateformat import format
import datetime
import os

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

EXTENSOES_PERMITIDAS = [
    "jpg", "jpeg", "png", "gif",   # imagens
    "mp4", "mov", "avi", "mkv",   # vídeos
    "mp3", "wav", "ogg",          # áudios
    "pdf",                        # documentos
    "pdf",                        # documentos
]

FORMATO_AUDIO_PERMITIDA = ["mp3", "ogg",]


def hoje():
    return datetime.date.today()


class Pessoa(models.Model):
    
    nome = models.CharField('Nome', max_length=100, null=False, blank=False)
    fones = models.CharField('Fone(s)',max_length=40, null=True, blank=True)
    email= models.EmailField('Email(s)',max_length=100, null=True, blank=True)
    naturalidade = models.CharField('Natural',max_length=40, null=True, blank=True)
    nacionalidade = models.CharField('Nacionalidade',max_length=20, null=True, blank=True)
    nascimento = models.DateField('Data de nascimento', null=True, blank=True, validators=[MaxValueValidator(limit_value=hoje)])
    biografia = models.TextField('Biografia',null=True, blank=False)
    pessoa_fisica = models.BooleanField('Pessoa física?',default=True, null=False)
    autor_de_obra = models.BooleanField('Autor de obra?',default=True, null=False)

    class Meta:
        verbose_name: "Pessoa"
        verbose_name_plural = "Pessoas" 

    def __str__(self):
        return self.nome


class EixoOrganizador(models.Model):
    
    eixo = models.CharField('Eixo', max_length=100, null=False, blank=False)    

    class Meta:
        verbose_name = "Eixo Organizador"
        verbose_name_plural = "Eixos Organizadores"

    def __str__(self):
        return self.eixo


class Exposicao(models.Model):
    
    nome = models.CharField('Exposição', max_length=200, null=False, blank=False)
    descricao = models.TextField('Descrição', null=False, blank=False)
    data_inicio = models.DateField('Data de início', null=False, blank=False)
    data_final = models.DateField('Data de encerramento', null=False, blank=False)
    local = models.CharField('Local(ais)', max_length=255, null=False, blank=False)
    orgazador = models.CharField('Organizador(es)', max_length=200, null=False, blank=False)
    exposicao_fisica = models.BooleanField('Exposicação física', default=True)

    class Meta:
        verbose_name = "Exposição"
        verbose_name_plural = "Exposições"

    def __str__(self):
        return f"{self.nome} de {format(self.data_inicio, 'd/m/Y')} à {format(self.data_final, 'd/m/Y')}"
    

class LocalInterno(models.Model):
    local = models.CharField('Local na ACORDE', max_length=100, null=False, blank=False)    

    class Meta:
        verbose_name = "Local Interno"
        verbose_name_plural = "Locais Internos"

    def __str__(self):
        return self.local
       

class PecasAcervo(models.Model):

    denominacao = models.CharField('Nome da peça',max_length=100, null=False, blank=False)
    autor = models.ManyToManyField(Pessoa, blank=True, verbose_name="Autores(as)")
    titulo_dado_pelo_autor = models.CharField('Título dado pelo autor', max_length=100, null=False, blank=False)
    nr_registro = models.CharField('Nº registro', max_length=10, null=True, blank=True)
    numero_ordem = models.CharField('Nº de ordem', max_length=3, null=True, blank=True)
    situacao = models.CharField('Situação',max_length=2, choices=SITUACAO.items(), default="LC")
    thesaurus = models.CharField('Thesaurus',max_length=100, null=True, blank=True)
    resumo_descritivo = models.TextField('Descrição', null=False, blank=False)
    dimensoes = models.CharField('Dimensões', max_length=30, null=True, blank=True)
    material_tecnica = models.TextField('Tipo de material e técnica',null=False, blank=False)
    estado_conservacao = models.CharField('Estado de conservação',max_length=3, choices=CONSERVACAO.items())
    local_producao = models.CharField('Local onde foi produzida', max_length=200, null=False, blank=False)
    data_inicial_producao = models.DateField('Data inicial produção',validators=[MaxValueValidator(limit_value=hoje)], null=True, blank=True)
    data_final_producao = models.DateField('Data final produção',validators=[MaxValueValidator(limit_value=hoje)], null=True, blank=True)
    pode_reproduzir = models.BooleanField('Pode reproduzir?',default=False, null=False)
    condicoes_reproducao = models.TextField('Condições da reprodução',null=True, blank=True)
    tipologia = models.CharField('Tipologia', max_length=3, choices=TIPOLOGIA.items(), default="MUS")
    forma_aquisicao = models.CharField('Forma de aquisição',max_length=3, null=False, blank=False, choices=AQUISICAO.items())
    eixo_organizador = models.ForeignKey(EixoOrganizador, null=True, blank=True, on_delete=models.SET_NULL)
    exposicao = models.ForeignKey(Exposicao, null=True, blank=True, on_delete=models.SET_NULL)
    localizacao_interna = models.ForeignKey(LocalInterno, null=True, blank=True, on_delete=models.SET_NULL)
    publicada = models.BooleanField('Publicar no site',default=False, null=False)

    class Meta:
        verbose_name = "Peça"
        verbose_name_plural = "Peças"

    def __str__(self):
        return self.denominacao
    

class Midia(models.Model):
    
    peca_acervo = models.ForeignKey(PecasAcervo, on_delete=models.CASCADE, null=False, blank=False, related_name="midias")
    tipo = models.CharField('Tipo da mídia', max_length=1, choices=TIPO_MIDIA_DIGITAL.items(), default="F", blank=False, null=False)
    url_midia = models.FileField('Arquivo', upload_to="acervo/", null=True, blank=False, validators=[FileExtensionValidator(allowed_extensions=EXTENSOES_PERMITIDAS)])
    data_upload = models.DateField('Data upload', auto_now_add=True)
    texto_descricao = models.TextField('Texto de descrição', blank=True)
    audio_descricao = models.FileField('Áudiodescrição', upload_to='acervo/audiodescricoes', validators=[FileExtensionValidator(allowed_extensions=FORMATO_AUDIO_PERMITIDA)], null=True, blank=True)
    qrcode_midia = models.ImageField('QRCode da mídia', upload_to='acervo/qrcodes', null=True, blank=True)
    
    class Meta:
        verbose_name = "Mídia"
        verbose_name_plural = "Mídias"
    legenda = models.CharField(max_length=120, null=True, blank=False)

    def __str__(self):
        return f"{TIPO_MIDIA_DIGITAL[self.tipo]} da(o) '{self.peca_acervo}'"

    def save(self, *args, **kwargs):
        if isinstance(self.url_midia, UploadedFile):
            self.url_midia.name = os.path.basename(self.url_midia.name)
            if self.pk:
                previous = type(self).objects.filter(pk=self.pk).only("url_midia").first()
                if previous and previous.url_midia:
                    previous.url_midia.delete(save=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.url_midia:
            self.url_midia.delete(save=False)
        if self.audio_descricao:
            self.audio_descricao.delete(save=False)
        if self.qrcode_midia:
            self.qrcode_midia.delete(save=False)
        return super().delete(*args, **kwargs)


class TipoEventoPeca(models.Model):

    desc_evento = models.CharField('Tipo do evento', max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = "Tipo do Evento da Peça"
        verbose_name_plural = "Tipos dos Eventos da Peça"

    def __str__(self):
        return self.desc_evento


class HistoricoPecas(models.Model):

    peca = models.ForeignKey(PecasAcervo, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEventoPeca, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.TextField('Detalhamento do evento', null=True, blank=True)
    data_inicio = models.DateField('Data de início', null=False, blank=False, default=datetime.date.today)
    data_final = models.DateField('Data final', null=False, blank=False, default=datetime.date.today)

    class Meta:
        verbose_name = "Histórico da Peça"
        verbose_name_plural = "Históricos da Peça"

    def __str__(self):
        return f"{self.peca} - {self.tipo_evento} - De {format(self.data_inicio, 'd/m/Y')} a {format(self.data_final, 'd/m/Y')}"

class Configs(models.Model):
    open_ia_key = models.TextField("Chave da OpenAI", blank=True, null=True)

    class Meta:
        verbose_name = "Configuracao do sistema"
        verbose_name_plural = "Configuracoes do sistema"

    def __str__(self):
        return "Configuracoes do sistema"
