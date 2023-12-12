from rest_framework import serializers
from django.db import transaction

from planetarium.models import Reservation, Ticket
from planetarium.serializers.ticket import (
    TicketListSerializer,
    TicketSerializer,
)


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def validate(self, attrs):
        tickets = attrs.get("tickets")
        show_session = tickets[0].get("show_session")
        for ticket in tickets:
            if ticket.get("show_session") != show_session:
                raise serializers.ValidationError("All tickets must be for the same show session")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Reservation.objects.create(**validated_data)

        for ticket_data in tickets_data:
            ticket_data["reservation"] = order
            Ticket.objects.create(**ticket_data)

        return order


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
