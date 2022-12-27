from rest_framework import serializers
from Vision.models import mangas


class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = mangas
        fields = "__all__"
