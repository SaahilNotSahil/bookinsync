from rest_framework import serializers

from .models import Bus, City, Route, Seat


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(
        source="all_seats",
        many=True,
        read_only=True
    )

    class Meta:
        model = Bus
        fields = '__all__'
        read_only_fields = ('remaining_seats', 'is_full')
