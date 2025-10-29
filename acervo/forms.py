from django import forms
from django.forms import inlineformset_factory

from .models import Midia, PecasAcervo, Pessoa, Exposicao, EixoOrganizador


class PecasAcervoForm(forms.ModelForm):
    data_inicial_producao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )
    data_final_producao = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = PecasAcervo
        fields = [
            "denominacao",
            "autor",
            "titulo_dado_pelo_autor",
            "nr_registro",
            "numero_ordem",
            "situacao",
            "thesaurus",
            "resumo_descritivo",
            "dimensoes",
            "material_tecnica",
            "estado_conservacao",
            "local_producao",
            "data_inicial_producao",
            "data_final_producao",
            "pode_reproduzir",
            "condicoes_reproducao",
            "tipologia",
            "forma_aquisicao",
            "eixo_organizador",
            "exposicao",
            "localizacao_interna",
            "publicada",
        ]
        labels = {
            "denominacao": "Denominação da peça",
            "autor": "Autores da obra",
            "titulo_dado_pelo_autor": "Título atribuído pelo autor(a)",
            "nr_registro": "Número de registro",
            "numero_ordem": "Número de ordem",
            "situacao": "Situação",
            "thesaurus": "Thesaurus",
            "resumo_descritivo": "Descrição",
            "dimensoes": "Dimensões",
            "material_tecnica": "Material e técnica",
            "estado_conservacao": "Estado de conservação",
            "local_producao": "Local de produção",
            "data_inicial_producao": "Data inicial de produção",
            "data_final_producao": "Data final de produção",
            "pode_reproduzir": "Pode reproduzir?",
            "condicoes_reproducao": "Condições para reprodução",
            "tipologia": "Tipologia",
            "forma_aquisicao": "Forma de aquisição",
            "eixo_organizador": "Eixo organizador",
            "exposicao": "Exposição",
            "localizacao_interna": "Localização interna",
            "publicada": "Publicar no site",
        }
        help_texts = {
            "autor": "Selecione um ou mais autores. Use Ctrl ou Command para múltipla seleção.",
            "thesaurus": "Informe termos controlados relacionados à peça.",
            "dimensoes": "Exemplo: 30 cm x 50 cm x 2 cm.",
            "condicoes_reproducao": "Descreva condições ou restrições para reprodução.",
        }
        error_messages = {
            "denominacao": {"required": "Informe a denominação da peça."},
            "titulo_dado_pelo_autor": {"required": "Informe o título atribuído pelo autor(a)."},
            "resumo_descritivo": {"required": "Descreva a peça."},
            "material_tecnica": {"required": "Informe o material e a técnica aplicados."},
            "estado_conservacao": {"required": "Selecione o estado de conservação da peça."},
            "local_producao": {"required": "Informe o local de produção da peça."},
            "forma_aquisicao": {"required": "Selecione a forma de aquisição da peça."},
        }
        widgets = {
            "resumo_descritivo": forms.Textarea(attrs={"rows": 3}),
            "material_tecnica": forms.Textarea(attrs={"rows": 3}),
            "condicoes_reproducao": forms.Textarea(attrs={"rows": 3}),
            "pode_reproduzir": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "publicada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    PLACEHOLDERS = {
        "denominacao": "Digite a denominação interna da peça",
        "titulo_dado_pelo_autor": "Informe o título atribuído pelo(a) autor(a)",
        "nr_registro": "Ex.: 1234-AB",
        "numero_ordem": "Ex.: 001",
        "thesaurus": "Termos controlados associados à peça",
        "resumo_descritivo": "Descreva a peça de forma objetiva",
        "dimensoes": "Ex.: 30 cm x 50 cm x 2 cm",
        "material_tecnica": "Detalhe materiais e técnicas utilizados",
        "local_producao": "Informe a cidade, estado ou país",
        "condicoes_reproducao": "Descreva as condições de uso e reprodução",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def add_class(widget, css_class):
            existing = widget.attrs.get("class", "")
            classes = existing.split()
            if css_class not in classes:
                classes.append(css_class)
            widget.attrs["class"] = " ".join(c for c in classes if c)

        for field_name, field in self.fields.items():
            if field_name in {"pode_reproduzir", "publicada"}:
                continue

            widget = field.widget
            if isinstance(widget, (forms.TextInput, forms.NumberInput, forms.EmailInput)):
                add_class(widget, "form-control")
            elif isinstance(widget, forms.Textarea):
                add_class(widget, "form-control")
            elif isinstance(widget, (forms.Select, forms.widgets.SelectMultiple)):
                add_class(widget, "form-select")

            placeholder = self.PLACEHOLDERS.get(field_name)
            if placeholder:
                widget.attrs.setdefault("placeholder", placeholder)

        for field_name in ["eixo_organizador", "exposicao", "localizacao_interna"]:
            self.fields[field_name].empty_label = "Selecione uma opção"

        if self.is_bound:
            for field_name, field in self.fields.items():
                if self.errors.get(field_name):
                    add_class(field.widget, "is-invalid")


class MidiaForm(forms.ModelForm):
    class Meta:
        model = Midia
        fields = ["tipo", "url_midia", "legenda"]
        labels = {
            "tipo": "Tipo da mídia",
            "url_midia": "Arquivo",
            "legenda": "Legenda",
        }
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "url_midia": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "legenda": forms.TextInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "url_midia": "Formatos aceitos: jpg, png, gif, mp4, mp3, pdf, etc.",
            "legenda": "Descreva brevemente o conteúdo da mídia.",
        }
        error_messages = {
            "url_midia": {"required": "Envie um arquivo para a mídia."},
        }


MidiaFormSet = inlineformset_factory(
    PecasAcervo,
    Midia,
    form=MidiaForm,
    extra=1,
    can_delete=True,
)

class PessoaForm(forms.ModelForm):
    nascimento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Pessoa
        fields = [
            "nome",
            "email",
            "fones",
            "naturalidade",
            "nacionalidade",
            "nascimento",
            "biografia",
            "pessoa_fisica",
            "autor_de_obra",
        ]
        labels = {
            "nome": "Nome completo",
            "fones": "Telefone(s)",
            "naturalidade": "Naturalidade",
            "nacionalidade": "Nacionalidade",
            "nascimento": "Data de nascimento",
            "biografia": "Biografia",
            "pessoa_fisica": "Pessoa física?",
            "autor_de_obra": "Autor(a) de obra?",
        }
        widgets = {
            "biografia": forms.Textarea(attrs={"rows": 4}),
            "pessoa_fisica": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "autor_de_obra": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "fones": "Informe um ou mais telefones. Separe por vírgula, se necessário.",
            "biografia": "Resumo da trajetória ou informações relevantes.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def add_class(widget, css_class):
            existing = widget.attrs.get("class", "")
            classes = existing.split()
            if css_class not in classes:
                classes.append(css_class)
            widget.attrs["class"] = " ".join(c for c in classes if c)

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                continue

            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.DateInput,
                ),
            ):
                add_class(widget, "form-control")
            elif isinstance(widget, forms.Textarea):
                add_class(widget, "form-control")

        if self.is_bound:
            for field_name, field in self.fields.items():
                if self.errors.get(field_name):
                    add_class(field.widget, "is-invalid")


class EixoOrganizadorForm(forms.ModelForm):
    class Meta:
        model = EixoOrganizador
        fields = ["eixo"]
        labels = {"eixo": "Eixo organizador"}
        error_messages = {
            "eixo": {"required": "Informe o eixo organizador."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def add_class(widget, css_class):
            existing = widget.attrs.get("class", "")
            classes = existing.split()
            if css_class not in classes:
                classes.append(css_class)
            widget.attrs["class"] = " ".join(c for c in classes if c)

        add_class(self.fields["eixo"].widget, "form-control")

        if self.is_bound and self.errors.get("eixo"):
            add_class(self.fields["eixo"].widget, "is-invalid")


class ExposicaoForm(forms.ModelForm):
    data_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )
    data_final = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Exposicao
        fields = [
            "nome",
            "descricao",
            "data_inicio",
            "data_final",
            "local",
            "orgazador",
        ]
        labels = {
            "nome": "Nome da exposição",
            "descricao": "Descrição",
            "data_inicio": "Data de início",
            "data_final": "Data de encerramento",
            "local": "Local(ais)",
            "orgazador": "Organizador(es)",
        }
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "local": "Informe o(s) local(ais) onde a exposição ocorreu ou ocorrerá.",
            "orgazador": "Informe o(s) organizador(es) da exposição.",
        }
        error_messages = {
            "nome": {"required": "Informe o nome da exposição."},
            "descricao": {"required": "Descreva a exposição."},
            "data_inicio": {"required": "Informe a data de início."},
            "data_final": {"required": "Informe a data de encerramento."},
            "local": {"required": "Informe o local da exposição."},
            "orgazador": {"required": "Informe o(s) organizador(es)."},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def add_class(widget, css_class):
            existing = widget.attrs.get("class", "")
            classes = existing.split()
            if css_class not in classes:
                classes.append(css_class)
            widget.attrs["class"] = " ".join(c for c in classes if c)

        for field_name, field in self.fields.items():
            widget = field.widget
            if isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.NumberInput,
                    forms.DateInput,
                ),
            ):
                add_class(widget, "form-control")
            elif isinstance(widget, forms.Textarea):
                add_class(widget, "form-control")

        if self.is_bound:
            for field_name, field in self.fields.items():
                if self.errors.get(field_name):
                    add_class(field.widget, "is-invalid")

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get("data_inicio")
        data_final = cleaned_data.get("data_final")

        if data_inicio and data_final and data_inicio > data_final:
            raise forms.ValidationError(
                "A data de encerramento deve ser posterior à data de início."
            )

        return cleaned_data
