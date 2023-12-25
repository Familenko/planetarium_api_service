from rest_framework import serializers

from planetarium.models import ShowTheme


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class ShowThemeListSerializer(ShowThemeSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class ShowThemeDetailSerializer(ShowThemeSerializer):
    shows = serializers.SerializerMethodField(method_name="get_shows")

    class Meta:
        model = ShowTheme
        fields = ("id", "name", "shows")

    def get_shows(self, obj):
        return obj.astronomy_show.all().values_list("title", flat=True)
