from rest_framework import serializers
from events.models import TicketCategory, Event
from .models import Booking
from events.serializers import TicketCategorySerializer, EventSerializer

class BookingSerializer(serializers.ModelSerializer):
    ticket_category = TicketCategorySerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    ticket_category_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketCategory.objects.all(),
        source="ticket_category",
        write_only=True
    )
    
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source="event",
        write_only=True
    )
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