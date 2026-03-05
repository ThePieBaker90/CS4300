from rest_framework import serializers
from .models import Movie, Seat, Booking

#Serializers for all of the objects we made earlier
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        #Good security, also the booking date should not be mutable. It is auto set when created.
        read_only_fields = ("user", "booking_date")