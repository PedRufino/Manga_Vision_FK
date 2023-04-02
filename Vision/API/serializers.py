from rest_framework import serializers
from Vision.models import mangas


class VisionSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    def get_genres(self, obj):
        return [genre.genero for genre in obj.genre.all()]

    class Meta:
        model = mangas
        fields = [
            "id_manga",
            "modified",
            "finished",
            "in_launch",
            "Abandoned",
            "title",
            "author",
            "release_Year",
            "type_manga",
            "genres",
            "responsible_Group",
            "sinopse",
            "capa",
            "slug",
        ]
