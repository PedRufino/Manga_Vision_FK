from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lista-de-titulos/", ListMangasView.as_view(), name="mangas.html"),
    path("historico-favoritos/", HistoricView.as_view(), name="historic.html"),
    path("meu-duo/", PartyView.as_view(), name="party.html"),
    path("me-ajude/", HelpView.as_view(), name="help.html"),
    path("store/", StoreView.as_view(), name="store.html"),
    path("contatos-e-outros/", contact, name="contato.html"),
    path("manga/<str:slug_>", manga_reading, name="manga_info"),
    path(
        "manga/<str:slug_>/ler/capitulo-<int:cap_>",
        chapter_reading,
        name="manga_chapter",
    ),
]
