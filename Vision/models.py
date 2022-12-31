from stdimage.models import StdImageField
from django.urls import reverse
from django.db import models
import os

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

# Criação das tabelas no Bando de dados
"""
    Tabela Abstrata
"""


class Base(models.Model):
    modified = models.DateField("Data de Atualização", auto_now=True)
    finished = models.BooleanField("Finalizado")
    in_launch = models.BooleanField("Lançamento", default=True)
    Abandoned = models.BooleanField("Abandonado")

    class Meta:
        abstract = True


"""
    Tabelas BD - Mangas
"""


def manga_directory_path(instance, filename):
    # define o caminho da pasta do livro como "books/<nome do livro>"
    return "mangas/{0}/{1}".format(instance.slug, filename)


def chapter_directory_path(instance):
    # define o caminho da pasta do capítulo como "books/<nome do livro>/chapters"
    return "mangas/{0}/capitulo-{1}".format(instance.manga.slug, instance.order)


def page_directory_path(instance, filename):
    # define o caminho da pasta do capítulo como "books/<nome do livro>/chapters"
    return "mangas/{0}/capitulo-{1}/{2}".format(instance.capitulo.manga.slug, instance.capitulo.order, filename)


class mangas(Base):
    id_manga = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    genre = models.ManyToManyField("genres")
    title = models.CharField("Nome do Manga", max_length=150, blank=True)
    author = models.CharField("Autor do Manga", max_length=150, blank=True)
    release_Year = models.IntegerField("Data de Lançamento", blank=True)
    responsible_Group = models.CharField("Nome do Grupo", max_length=150, blank=True)
    sinopse = models.TextField("Sinopse", blank=True)
    capa = StdImageField("Capas dos Mangas", upload_to=manga_directory_path)
    slug = models.SlugField("Slug", max_length=150, blank=True, editable=True, unique=True)
    rank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # atualiza o slug do livro usando o título e o slugify
        self.slug = slugify(self.title)

        # cria a pasta do livro caso ela não exista
        if not os.path.exists(os.path.join("media", "mangas", self.slug)):
            os.makedirs(os.path.join("media", "mangas", self.slug))
        super(mangas, self).save(*args, **kwargs)


class Chapter(models.Model):
    capitulo = models.CharField(blank=True, max_length=150)
    order = models.PositiveIntegerField()
    texto = models.TextField(blank=True)
    manga = models.ForeignKey(mangas, on_delete=models.CASCADE)

    def __str__(self):
        return f"Capitulo-{self.order} Manga: {self.manga}"

    def save(self, *args, **kwargs):
        # cria a pasta do capítulo caso ela não exista
        if not os.path.exists(os.path.join("media", "mangas", self.manga.slug, f"capitulo-{self.order}")):
            os.makedirs(os.path.join("media", "mangas", self.manga.slug, f"capitulo-{self.order}"))
        super(Chapter, self).save(*args, **kwargs)

    class Meta:
        # ordena os capítulos pelo campo "order"
        ordering = ["order"]


class Pagina(models.Model):
    pg_name = models.CharField(blank=True, max_length=150)
    order = models.PositiveIntegerField()
    imagem = StdImageField("Paginas", upload_to=page_directory_path)
    capitulo = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # cria a pasta do capítulo caso ela não exista
        if not os.path.exists(os.path.join("media","mangas",self.capitulo.manga.slug,f"capitulo-{self.capitulo.order}",)):
            os.makedirs(os.path.join("media","mangas",self.capitulo.manga.slug,f"capitulo-{self.capitulo.order}",))
        super(Pagina, self).save(*args, **kwargs)

    class Meta:
        # ordena os capítulos pelo campo "order"
        ordering = ["order"]


class genres(models.Model):
    id_gender = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    genero = models.CharField("Generos", max_length=150)

    def __str__(self):
        return self.genero


class VisionMangasGenre(models.Model):
    id = models.BigAutoField(primary_key=True)
    mangas = models.ForeignKey(mangas, models.DO_NOTHING)
    genres = models.ForeignKey(genres, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "vision_mangas_genre"
        unique_together = (("mangas", "genres"),)


class ClickManga(models.Model):
    manga = models.ForeignKey(mangas, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)


"""
    Tabela BD - Contatos
"""


class FormContato(models.Model):
    nome = models.CharField("Nome", max_length=150)
    email = models.CharField("E-mail", max_length=150)
    assunto = models.CharField("Assunto", max_length=100)
    mensagem = models.TextField("Mensagem")
    data_envio = models.DateTimeField("Data do Envio", auto_now_add=True)
    resolvido = models.BooleanField("Resolvido", default=False)


"""
    Tabela BD - Comentarios
"""


# class Comments(models.Model):
#     title = models.CharField(max_length=255, unique=True)
#     slug = models.SlugField(max_length=255)
#     body = models.TextField()
#     posted = models.DateField(db_index=True, auto_now_add=True)
#     description = models.CharField(max_length=255,null=True)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('blog:detail',kwargs={'slug':self.slug})
