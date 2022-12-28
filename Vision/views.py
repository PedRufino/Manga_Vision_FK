from django.views.generic import TemplateView
from .forms import ContatoModelForm
from django.shortcuts import render
from django.contrib import messages
from .models import mangas, ClickManga
from datetime import date, timedelta


def manga_reading(request, slug_):
    manga = mangas.objects.get(slug=slug_)
    manga.rank += 1
    manga.save()

    click = ClickManga(manga=manga)
    click.save()
    return render(request, "manga_reading.html")


class IndexView(TemplateView):
    template_name = "index.html"
    
    def manga_date(self):
        start_date = date.today()
        end_date = start_date - timedelta(days=7)
        manga_data = mangas.objects.filter(modified__range=[end_date, start_date])

        TodayManga = []
        count = 1
        for mgDate in manga_data:
            count += 1
            genre_list = []
            for gen in mgDate.genre.all():
                genre_list.append(str(gen))
            genre = ", ".join(genre_list)

            mg_all = {
                "id_manga": mgDate.id_manga,
                "title": mgDate.title,
                "genero": genre,
                "data": mgDate.modified,
                "sinopse": mgDate.sinopse,
                "slug": mgDate.slug,
                "url_img": mgDate.capa,
            }

            TodayManga.append(mg_all)
        return TodayManga

    def mais_lidos(self):
        MaisLidos = []
        img = [
            "../static/img/trofeus/taca-de-ouro.png",
            "../static/img/trofeus/taca-de-prata.png",
            "../static/img/trofeus/taca-de-bronze.png",
        ]
        most_read = mangas.objects.all().order_by("-rank")[:3]
        x = 0
        for mgl in most_read:
            genre_list = []
            for gen in mgl.genre.all():
                genre_list.append(str(gen))
            genre = ", ".join(genre_list)

            dict_ = {
                "title": mgl.title,
                "slug": mgl.slug,
                "url_img": mgl.capa,
                "genero": genre,
                "url_trofeu": img[x],
                "rank": mgl.rank,
            }
            MaisLidos.append(dict_)
            x += 1
        return MaisLidos

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['all_mangas'] = mangas.objects.all()
        context['lancamentos'] = self.manga_date()
        context['mais_lidos'] = self.mais_lidos()
        return context


class MangasView(TemplateView):
    template_name = "mangas.html"


class PartyView(TemplateView):
    template_name = "party..html"


class HelpView(TemplateView):
    template_name = "help.html"


class HistoricView(TemplateView):
    template_name = "historic.html"


def contact(request):
    if str(request.method) == "POST":
        form = ContatoModelForm(request.POST, request.FILES)
        if form.is_valid():

            form.save()

            messages.success(request, "E-mail enviando com sucesso.")
            form = ContatoModelForm()
        else:
            messages.error(request, "Erro ao enviar o E-mail.")
    else:
        form = ContatoModelForm()
    context = {"form": form}
    return render(request, "contato.html", context)
