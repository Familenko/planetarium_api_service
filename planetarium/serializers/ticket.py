from rest_framework import serializers

from planetarium.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("show_session", "row", "seat")

    def validate(self, attrs):
        row = attrs.get("row")
        seat = attrs.get("seat")
        show_session = attrs.get("show_session")

        if row < 0:
            raise serializers.ValidationError("Row can't be negative")
        if seat < 0:
            raise serializers.ValidationError("Seat can't be negative")

        if row > show_session.planetarium_dome.rows:
            raise serializers.ValidationError("Row can't be bigger than rows in dome")
        if seat > show_session.planetarium_dome.seats_in_row:
            raise serializers.ValidationError("Seat can't be bigger than seats in row")

        is_unique = (
            Ticket.objects.filter(show_session=show_session, row=row, seat=seat).count()
            == 0
        )
        if not is_unique:
            raise serializers.ValidationError("Ticket already exists")

        return attrs


class TicketListSerializer(TicketSerializer):
    show_session = serializers.StringRelatedField(many=False, read_only=True)
    reservation = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "reservation", "show_session", "row", "seat")


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")
