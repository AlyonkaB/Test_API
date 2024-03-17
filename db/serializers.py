from rest_framework import serializers

from db.models import Bus, Trip, Facility


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
        fields = ("id", "info", "num_seat", "is_mini", "facility")


class BusListSerializer(BusSerializer):
    # facility = serializers.StringRelatedField(many=True)
    facility = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )


class BusDetailSerializer(BusSerializer):
    facility = FacilitySerializer(many=True, read_only=True)


class TripSerializer(serializers.ModelSerializer):
    # bus = BusSerializer(many=False, read_only=True) #тільки 1 обьєкт і тільки для відобрачення, але не для створення
    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")


class TripListSerializer(TripSerializer):
    bus_info = serializers.CharField(source="bus.info", read_only=True)
    bus_num_seats = serializers.IntegerField(source="bus.num_seat", read_only=True)

    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus_info", "bus_num_seats")


class TripDetailSerializer(TripSerializer):
    bus = BusDetailSerializer(many=False, read_only=True)
