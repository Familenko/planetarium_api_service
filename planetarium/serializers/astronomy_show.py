from rest_framework import serializers

from planetarium.models import AstronomyShow


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "show_themes")


class AstronomyShowDetailSerializer(AstronomyShowListSerializer):
    show_themes = serializers.StringRelatedField(many=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_themes")
