from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lista-de-titulos/A-Z", ListMangasView.as_view(), name="mangas.html"),
    path("lista-de-titulos/<str:order>", ListMangasView.as_view(), name="alpha_beto.html"),
    path("lista-de-titulos/A-Z/search-genero/<str:id_genre>", ListMangasView.as_view(), name="genre_list.html"),
    path('lista-de-titulos/A-Z/search/', MangasSearchView.as_view(), name='manga_search.html'),
    path("store/", StoreView.as_view(), name="store.html"),
    path("contatos-e-outros/", contact, name="contato.html"),
    path("manga/<str:slug_>", manga_reading, name="manga_info"),
    path("manga/<str:slug_>/<str:rate>", save_rating, name="manga_info"),
    path(
        "manga/<str:slug_>/ler/capitulo-<int:cap_>",
        chapter_reading,
        name="manga_chapter",
    ),
]
