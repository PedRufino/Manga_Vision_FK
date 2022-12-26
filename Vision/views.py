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
    return render(request, 'manga_reading.html')

def index(request):
    manga = mangas.objects.all()
    '''
        Retorna uma lista de tuplas com as informações dos mangas + generos formatados
    '''
    all_mangas = []
    for item in manga:
        genre_list = []
        for gen in item.genre.all():
            genre_list.append(str(gen))
        genre = ', '.join(genre_list)
        
        mg_all = {
            'id_manga': item.id_manga,
            'title': item.title,
            'genero': genre,
            'data': item.modified,
            'sinopse': item.sinopse,
            'slug': item.slug,
            'url_img': item.capa,
        }
        
        all_mangas.append(mg_all)
    
    '''
        Retorna uma lista de tuplas de 3 Mangas com infos e com datas dos ultimos 7 dias
    '''
    startdate = date.today()
    enddate = startdate - timedelta(days=7)
    manga_data = mangas.objects.filter(modified__range=[enddate, startdate])
    
    TodayManga = []
    count = 1
    for mgDate in manga_data:
        count += 1
        genre_list = []
        for gen in mgDate.genre.all():
            genre_list.append(str(gen))
        genre = ', '.join(genre_list)
        
        mg_all = {
            'id_manga': mgDate.id_manga,
            'title': mgDate.title,
            'genero': genre,
            'data': mgDate.modified,
            'sinopse': mgDate.sinopse,
            'slug': mgDate.slug,
            'url_img': mgDate.capa,
        }
        
        TodayManga.append(mg_all)
    
    MaisLidos = []
    img = ['../static/img/trofeus/taca-de-ouro.png', '../static/img/trofeus/taca-de-prata.png', '../static/img/trofeus/taca-de-bronze.png']
    most_read = mangas.objects.all().order_by('-rank')[:3]
    x = 0
    for mgl in most_read:
        genre_list = []
        for gen in mgl.genre.all():
            genre_list.append(str(gen))
        genre = ', '.join(genre_list)
        
        dict_={
            'title': mgl.title,
            'slug': mgl.slug,
            'url_img': mgl.capa,
            'genero': genre,
            'url_trofeu': img[x],
            'rank': mgl.rank,
        }
        MaisLidos.append(dict_)
        x += 1
    
    context = {
        'all_mangas_list': all_mangas,
        'Lancamentos': TodayManga,
        'MaisLidos': MaisLidos,
    }
    
    return render(request, 'index.html', context)


class MangasView(TemplateView):
    template_name = 'mangas.html'


class PartyView(TemplateView):
    template_name = 'party.html'


class HelpView(TemplateView):
    template_name = 'help.html'


class HistoricView(TemplateView):
    template_name = 'historic.html'


def contact(request):
    if str(request.method) == 'POST':
        form = ContatoModelForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            
            messages.success(request, 'E-mail enviando com sucesso.')
            form = ContatoModelForm()
        else:
            messages.error(request, 'Erro ao enviar o E-mail.')
    else:
        form = ContatoModelForm()
    context = {
        'form': form
    }
    return render(request, 'contato.html', context)