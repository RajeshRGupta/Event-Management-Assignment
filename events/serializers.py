from datetime import date
from rest_framework import serializers
from .models import Event, TicketCategory


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["organizer"]
    
    def validate_event_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Past date is not allowed."
            )
        return value

    def validate(self, data):
        venue = data.get("venue", self.instance.venue if self.instance else None)
        event_date = data.get("event_date",self.instance.event_date if self.instance else None)
        start = data.get("start_time",self.instance.start_time if self.instance else None)
        end = data.get("end_time",self.instance.end_time if self.instance else None)
        if start >= end:
            raise serializers.ValidationError(
                "End time must be greater than start time."
            )
        events = Event.objects.filter(venue=venue,event_date=event_date)
        if self.instance:
            events = events.exclude(id=self.instance.id)
            
        for event in events:
            if start < event.end_time and end > event.start_time:
                raise serializers.ValidationError(
                    "Venue already booked."
                )
        return data

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = "__all__"