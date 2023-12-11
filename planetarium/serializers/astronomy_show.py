from rest_framework import serializers

from planetarium.models import AstronomyShow


class AstronomyShowSerializer(serializers.ModelSerializer):
    show_theme = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_theme = serializers.StringRelatedField(
        source="show_themes", many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "show_theme")


class AstronomyShowDetailSerializer(AstronomyShowListSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme")
