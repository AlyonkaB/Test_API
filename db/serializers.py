from rest_framework import serializers

from db.models import Bus, Trip


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

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ("id", "info", "num_seat", "is_mini")


class TripSerializer(serializers.ModelSerializer):
    # bus = BusSerializer(many=False, read_only=True) #тільки 1 обьєкт і тільки для відобрачення, але не для створення
    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")

class TripListSerializer(TripSerializer):
    bus = BusSerializer(many=False, read_only=True)
