from django.contrib import admin
from .models import *


@admin.register(mangas)
class mangasAdmin(admin.ModelAdmin):
    list_display = (
        "id_manga",
        "title",
        "author",
        "modified",
        "slug",
        "in_launch",
        "finished",
        "Abandoned",
    )


@admin.register(FormContato)
class FormContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "assunto", "mensagem", "data_envio", "resolvido")


@admin.register(genres)
class genresAdmin(admin.ModelAdmin):
    list_display = ("id_gender", "genero")


@admin.register(Chapter)
class genresAdmin(admin.ModelAdmin):
    list_display = ("id","capitulo", "order", "texto", "manga")


@admin.register(Pagina)
class genresAdmin(admin.ModelAdmin):
    list_display = ("pg_name", "order", "imagem", "capitulo")


@admin.register(MangaRating)
class MangaRatingAdmin(admin.ModelAdmin):
    list_display = ("manga", "rating", "created_at")

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("manga", "rank")

@admin.register(store)
class RankAdmin(admin.ModelAdmin):
    list_display = ("titulo", "valor", "link_img", "link_vitrine")
