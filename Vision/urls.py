from django.urls import path
from .views import (
    IndexView,
    MangasView,
    PartyView,
    HelpView,
    HistoricView,
    contact,
    manga_reading,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lista-de-titulos/", MangasView.as_view(), name="mangas.html"),
    path("historico-favoritos/", HistoricView.as_view(), name="historic.html"),
    path("meu-duo/", PartyView.as_view(), name="party.html"),
    path("me-ajude/", HelpView.as_view(), name="help.html"),
    path("contatos-e-outros/", contact, name="contato.html"),
    path("manga/<str:slug_>", manga_reading, name="produto"),
]
