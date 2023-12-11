

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers


from planetarium.models import PlanetariumDome


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "capacity")

    def validate(self, attrs):
        capacity = attrs.get("capacity")
        if capacity < 0:
            raise serializers.ValidationError("Capacity can't be negative")
        return attrs
