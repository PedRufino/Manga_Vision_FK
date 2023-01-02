from django.views.generic import TemplateView
from .forms import ContatoModelForm
from django.shortcuts import render
from django.contrib import messages
from .models import mangas, ClickManga, Chapter, Pagina
from datetime import date, timedelta
from django.http import HttpResponse


# http://192.168.99.112:8000/manga/solo-leveling/#01/!page1



def manga_reading(request, slug_):
    # traz informações do manga selecionado
    manga = mangas.objects.get(slug=slug_)
    chap_all = Chapter.objects.all()
    manga.rank += 1
    manga.save()

    # Adiciona 1 ponto para o manga selecionado
    click = ClickManga(manga=manga)
    click.save()
    
    # leva o conteudo do chap_all para o html
    context = {
        'capiulo':chap_all,
        'manga': manga,
    }
    return render(request, "manga_info.html", context)


def chapter_reading(request, slug_, cap_):
    manga = mangas.objects.get(slug=slug_)
    chapter = Chapter.objects.get(order=cap_)
    page = Pagina.objects.all().filter(capitulo=chapter)
    context = {
        'manga':manga,
        'chapter': chapter,
        'page': page,
    }
    return render(request, "page_reading.html", context)

class IndexView(TemplateView):
    template_name = "index.html"
    
    def manga_date(self):
        start_date = date.today()
        end_date = start_date - timedelta(days=6)
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


class ListMangasView(TemplateView):
    template_name = "mangas.html"


class PartyView(TemplateView):
    template_name = "party..html"


class HelpView(TemplateView):
    template_name = "help.html"


class HistoricView(TemplateView):
    template_name = "historic.html"


class ComentView(TemplateView):
    template_name = "comentarios.html"


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
