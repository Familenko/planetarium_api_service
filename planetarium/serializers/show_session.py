from django.utils import timezone
from rest_framework import serializers

from planetarium.models import ShowSession
from planetarium.serializers.astronomy_show import AstronomyShowSerializer
from planetarium.serializers.planetarium_dome import PlanetariumDomeSerializer
from planetarium.serializers.ticket import TicketSeatsSerializer


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = "__all__"

    def validate(self, attrs):
        show_time = attrs.get("show_time")
        if show_time < timezone.now():
            raise serializers.ValidationError("You can't create show session in the past")
        return attrs


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)

    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time", "taken_places")


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = serializers.StringRelatedField(many=False, read_only=True)
    planetarium_dome = serializers.StringRelatedField(many=False, read_only=True)
    tickets_available = serializers.SerializerMethodField(
        method_name="get_tickets_available"
    )

    def get_tickets_available(self, obj):
        return obj.planetarium_dome.capacity - obj.tickets.count()

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
            "tickets_available",
        )
