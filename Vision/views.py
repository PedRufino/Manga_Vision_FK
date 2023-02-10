from django.views.generic import TemplateView
from .forms import ContatoModelForm
from django.shortcuts import render
from django.contrib import messages
from .models import mangas, ClickManga, Chapter, Pagina, Rank
from datetime import date, timedelta


def manga_reading(request, slug_):
    # traz informações do manga selecionado
    manga = mangas.objects.get(slug=slug_)
    chap_all = Chapter.objects.filter(manga=manga)

    # Adiciona 1 ponto para o manga selecionado
    try:
        rank_ = Rank.objects.get(manga=manga)
        rank_.rank += 1
        rank_.save()
    except Exception as erro:
        Rank.objects.create(manga=manga, rank=1)
    
    genre = manga.genre.values_list('genero', flat=True)
    
    #Status
    if manga.in_launch == True:
        status = "Em Lançamento"
    elif manga.Abandoned == True:
        status = "Abandonado"
    elif manga.finished == True:
        status = "Finalizado"
    
    # leva o conteudo do chap_all para o html
    context = {
        'capitulo':chap_all,
        'first':chap_all.first(),
        'last':chap_all.last(),
        'status': status,
        'manga': manga,
        'genre': genre,
    }
    return render(request, "manga_info.html", context)


def chapter_reading(request, slug_, cap_):
    manga = mangas.objects.get(slug=slug_)
    chapter = Chapter.objects.get(order=cap_, manga=manga)
    page = Pagina.objects.filter(capitulo=chapter)
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

        TodayManga = [
            {
                "id_manga": mgDate.id_manga,
                "title": mgDate.title,
                "genero": ", ".join(map(str, mgDate.genre.all())),
                "data": mgDate.modified,
                "sinopse": mgDate.sinopse,
                "slug": mgDate.slug,
                "url_img": mgDate.capa,
            }
            for mgDate in manga_data
        ]
        return TodayManga

    def mais_lidos(self):
        img = [
            "../static/img/trofeus/taca-de-ouro.png",
            "../static/img/trofeus/taca-de-prata.png",
            "../static/img/trofeus/taca-de-bronze.png",
        ]
        MaisLidos = [
            {
                "title": mgl.title,
                "slug": mgl.slug,
                "url_img": mgl.capa,
                "genero": ", ".join(map(str, mgl.genre.all())),
                "url_trofeu": img[x],
                # "rank": mgl.rank,
            }
            for x, mgl in enumerate(mangas.objects.all().order_by("-rank")[:3])
        ]
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
