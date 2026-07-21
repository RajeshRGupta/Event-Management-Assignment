from rest_framework import serializers
from .models import Booking
from events.serializers import TicketCategorySerializer, EventSerializer

class BookingSerializer(serializers.ModelSerializer):
    tiket_categoty = TicketCategorySerializer(read_only=True)
    event = EventSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = [
            "user",
            "total_amount",
            "status"
        ]
        
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value