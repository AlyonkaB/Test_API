from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from db.models import Bus, Trip, Facility, Ticket, Order


# class BusSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     info = serializers.CharField(required=False)
#     num_seat = serializers.IntegerField(required=True)
#
#     def create(self, validated_data):
#         return Bus.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.info = validated_data.get("info", instance.info)
#         instance.num_seat = validated_data.get("num_seat", instance.num_seat)
#         instance.save()
#         return instance
# _________________________________________________________________________________________________________
class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name")


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ("id", "info", "num_seat", "is_mini", "facility", "image")


class BusListSerializer(BusSerializer):
    # facility = serializers.StringRelatedField(many=True)
    facility = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )


class BusDetailSerializer(BusSerializer):
    facility = FacilitySerializer(many=True, read_only=True)


class BusImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ("id", "image")


class TripSerializer(serializers.ModelSerializer):
    # bus = BusSerializer(many=False, read_only=True) тільки 1 обьєкт і тільки для відобрачення, але не для створення
    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")


class TripListSerializer(TripSerializer):
    bus_info = serializers.CharField(source="bus.info", read_only=True)
    bus_num_seats = serializers.IntegerField(source="bus.num_seat", read_only=True)
    tickets_available = serializers.IntegerField( read_only=True)

    class Meta:
        model = Trip
        fields = (
            "id",
            "source",
            "destination",
            "departure",
            "bus_info",
            "bus_num_seats",
            "tickets_available"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=['seat', 'trip']
            )
        ]

    def validate(self, attrs) -> None:
        Ticket.validate_seat(
            attrs["seat"],
            attrs["trip"].bus.num_seat,
            serializers.ValidationError
        )
        # if not(1 <= attrs["seat"] <= attrs["trip"].bus.num_seat):
        #     raise serializers.ValidationError({
        #         "seat": f"seat be in range [1, {attrs['trip'].bus.num_seat}], not {attrs['seat']}"
        #     })


class TripDetailSerializer(TripSerializer):
    bus = BusDetailSerializer(many=False, read_only=True)
    taken_seats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="seat",
        source="tickets"
    )

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus", "taken_seats")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop('tickets')
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class TicketsListSerializers(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class OrderListSerializers(OrderSerializer):
    tickets = TicketsListSerializers(read_only=True, many=True)

