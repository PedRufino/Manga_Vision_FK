from django.urls import path
from .views import (
    IndexView,
    ListMangasView,
    PartyView,
    HelpView,
    HistoricView,
    ComentView,
    manga_reading,
    contact,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lista-de-titulos/", ListMangasView.as_view(), name="mangas.html"),
    path("historico-favoritos/", HistoricView.as_view(), name="historic.html"),
    path("meu-duo/", PartyView.as_view(), name="party.html"),
    path("me-ajude/", HelpView.as_view(), name="help.html"),
    path("comentario/", ComentView.as_view(), name="comentario.html"),
    path("contatos-e-outros/", contact, name="contato.html"),
    path("manga/<str:slug_>", manga_reading, name="manga"),
    path("manga/<str:slug_>/#<int:cap_>", manga_reading, name="manga_chapter"),
]
