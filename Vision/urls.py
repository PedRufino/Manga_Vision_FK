from django.urls import path
from .views import index, list_mangas, historic, party, help_me, contact, manga_reading

urlpatterns = [
    path('', index, name='index'),
    path('lista-de-titulos/', list_mangas, name='mangas.html'),
    path('historico-favoritos/', historic, name='historic.html'),
    path('meu-duo/', party, name='party.html'),
    path('me-ajude/', help_me, name='help.html'),
    path('contatos-e-outros/', contact, name='contato.html'),
    path('manga/<str:slug_>', manga_reading, name='produto'),
]
