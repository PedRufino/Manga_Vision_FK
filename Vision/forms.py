from .models import mangas, FormContato
from django import forms


class MangasModelForm(forms.ModelForm):
    class Meta:
        model = mangas
        fields = [
            "title",
            "author",
            "release_Year",
            "responsible_Group",
            "genre",
            "sinopse",
            "capa",
            "in_launch",
            "Abandoned",
            "finished",
        ]


class ContatoModelForm(forms.ModelForm):
    class Meta:
        model = FormContato
        fields = ["nome", "email", "assunto", "mensagem"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nome"].label = "Nome:"
        self.fields["email"].label = "E-mail:"
        self.fields["assunto"].label = "Assunto:"
        self.fields["mensagem"].label = "Mensagem:"

        self.fields["nome"].widget.attrs.update({"placeholder": "Digite seu nome..."})
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Digite seu e-mail..."}
        )
        self.fields["assunto"].widget.attrs.update(
            {"placeholder": "Digite o assunto..."}
        )
        self.fields["mensagem"].widget.attrs.update(
            {"class": "form-vision", "placeholder": "Digite sua mensagem..."}
        )
