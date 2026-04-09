from django.db import transaction
from rest_framework import serializers

from .models import Event, Reservation


class EventSerializer(serializers.ModelSerializer):
    reservations_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        if data.get('available_seats', 0)> data.get('total_seats', 0):
            raise serializers.ValidationError(
                {"available_seats cannot exceed total seats."}
            )

        return data

    def get_reservations_count(self, obj):
        return obj.reservations.filter(status='cpnformed').count()


class ReservationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "event",
            "event_title",
            "attendee_name",
            "attendee_email",
            "seats_reserved",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "event_title"]

    def validate_seats_reserved(self, value):
        if value <= 0:
            raise serializers.ValidationError("Seats reserved must be greater than zero.")
        return value
    def validate(self, data):
        # validate seat count
        event = data.get('event')
        if event.status not in ['upcoming', 'ongoing']:
            raise serializers.ValidationError(f"Cannot make reservation for an event that is {event.status}.")
        if data.get('seats_reserved', 0) > event.available_seats:
            raise serializers.ValidationError(f'only {event.available_seats} seats are available for this event.')
        return data
    def create(self , validated_data):
        seats_reserved = validated_data['seats_reserved']

        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=validated_data['event'].pk)

            if seats_reserved > event.available_seats:
                raise serializers.ValidationError(
                    {'seats_reserved': f'Only {event.available_seats} seats are available for this event.'}
                )

            event.available_seats -= seats_reserved
            event.save(update_fields=['available_seats'])
            validated_data['event'] = event

            return Reservation.objects.create(**validated_data)