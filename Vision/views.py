from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, View
from .forms import ContatoModelForm
from django.shortcuts import render
from django.contrib import messages
from .models import mangas, Chapter, Pagina, Rank, store, genres
from django.http import JsonResponse
from datetime import date, timedelta
from django.db.models import F
from django.conf import settings


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

    genre = manga.genre.values_list("genero", flat=True)

    # Status
    if manga.in_launch == True:
        status = "Em Lançamento"
    elif manga.Abandoned == True:
        status = "Abandonado"
    elif manga.finished == True:
        status = "Finalizado"

    # leva o conteudo do chap_all para o html
    context = {
        "capitulo": chap_all,
        "first": chap_all.first(),
        "last": chap_all.last(),
        "status": status,
        "manga": manga,
        "genre": genre,
    }
    return render(request, "manga_info.html", context)


def chapter_reading(request, slug_, cap_):
    manga = mangas.objects.get(slug=slug_)
    chapter = Chapter.objects.get(order=cap_, manga=manga)
    page = Pagina.objects.filter(capitulo=chapter)
    context = {
        "manga": manga,
        "chapter": chapter,
        "page": page,
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
            for x, mgl in enumerate(mangas.objects.annotate(ranking=F('rank__rank')).order_by('-ranking')[:3])
            
        ]
        return MaisLidos

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["all_mangas"] = mangas.objects.all().order_by('author')[:15]
        context["lancamentos"] = self.manga_date()
        context["mais_lidos"] = self.mais_lidos()
        return context


class ListMangasView(ListView):
    template_name = "mangas.html"
    paginate_by = 28
    model = mangas
    ordering = "id_manga"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        letra = self.kwargs.get('order')
        id_genre = self.kwargs.get('id_genre')
        
        if id_genre:
            model = mangas.objects.filter(genre__id_gender=id_genre).order_by('title')
            return model
        
        if letra:
            model = mangas.objects.filter(title__istartswith=letra).order_by('title')
        elif letra == 'numero':
            model = mangas.objects.filter(title__istartswith='-').order_by('title')
        elif letra == "A-Z":
            model = mangas.objects.all().order_by(self.ordering)
        else:
            model = mangas.objects.all().order_by(self.ordering)
        return model
    
    
    def mais_lidos(self):
        img = [
            "/static/img/trofeus/taca-de-ouro.png",
            "/static/img/trofeus/taca-de-prata.png",
            "/static/img/trofeus/taca-de-bronze.png",
        ]
        MaisLidos = [
            {
                "title": mgl.title,
                "slug": mgl.slug,
                "url_img": mgl.capa,
                "genero": ", ".join(map(str, mgl.genre.all())),
                "url_trofeu": img[x] if x < len(img) else '',
                # "rank": mgl.rank,
            }
            for x, mgl in enumerate(mangas.objects.annotate(ranking=F('rank__rank')).order_by('-ranking')[:10])
        ]
        return MaisLidos

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context["mais_lidos"] = self.mais_lidos()
        context["alpha"] = ['A-Z','#','A','B','C','D','E']
        context["alpha2"] = ['F','G','H','I','J','K','L']
        context["alpha3"] = ['M','N','O','P','Q','R','S']
        context["alpha4"] = ['T','U','V','W','X','Y','Z']
        context["genres"] = genres.objects.all()
        return context
    
class MangasSearchView(ListView):
    template_name = 'mangas.html'

    def get(self, request):
        manga_name = request.GET.get('manga_name')
        mangasList = mangas.objects.all().order_by('id_manga')[:28]
        
        if manga_name:
            mangasList = mangas.objects.filter(title__istartswith=manga_name)[:28]
        
        manga_list = []
        
        for mangaone in mangasList:
            manga_data = {
                'id_manga': mangaone.id_manga,
                'title': mangaone.title,
                'capa': request.build_absolute_uri(mangaone.capa.url),
            }
            manga_list.append(manga_data)
        
        return JsonResponse(manga_list, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['is_paginated'] = False
        return context

class StoreView(ListView):
    template_name = "store.html"
    paginate_by = 25
    model = store
    ordering = "id"


class PartyView(TemplateView):
    template_name = "party.html"


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
