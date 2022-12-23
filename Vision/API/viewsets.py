from rest_framework import viewsets
from Vision.API import serializers
from Vision import models

class VisionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VisionSerializer
    
    def get_queryset(self):
        queryset = models.mangas.objects.all()
        id_manga = self.request.query_params.get('id_manga')
        title_manga = self.request.query_params.get('title')
        
        if id_manga:
            queryset = models.mangas.objects.filter(id_manga=id_manga)
        
        if title_manga:
            # queryset = models.mangas.objects.filter(Title=title_manga)  # Pesquisa o title escrevido (Inteiro)
            # queryset = models.mangas.objects.filter(Title__contains=title_manga)  # Pesquisa com trecho ou palavras inteira
            # queryset = models.mangas.objects.filter(Title__startswith=title_manga) # Pesquisa se a Letra ou palavara começar em Maiúsculas (Letra, Trecho ou Palavra)
            queryset = models.mangas.objects.filter(title__istartswith=title_manga) # Pesquisa se a Letra ou palavara começar em Maiúsculas ou minúscula (Letra, Trecho ou Palavra)
        
        return queryset


# Site usado para pesquisa de QuerySets
# https://docs.djangoproject.com/en/4.1/ref/models/querysets/#std-fieldlookup-contains