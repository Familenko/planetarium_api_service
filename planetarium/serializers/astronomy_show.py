from rest_framework import serializers

from planetarium.models import AstronomyShow


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "duration", "themes", "age_limit")

    def validate(self, attrs):
        duration = attrs.get("duration")
        if duration < 0:
            raise serializers.ValidationError("Duration can't be negative")
        return attrs
