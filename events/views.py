from datetime import date,datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Event, TicketCategory
from .serializers import EventSerializer, TicketCategorySerializer


class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "organizer":
            events = Event.objects.filter(organizer=request.user)
        else:
            events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        # print("Organizer's events:", events[0].vanue)
        
        return Response(serializer.data)

    def post(self, request):
        print("Request data:", request.data)
        if request.user.role != "organizer":
            return Response(
                {"message": "Only organizer can create event."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                organizer=request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        

class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EventSerializer(event)
        
        data=serializer.data
        data["ticket_categories"] = TicketCategorySerializer(
            TicketCategory.objects.filter(event=event),
            many=True
        ).data
        
        print("Event details:", serializer.data)
        
        return Response(data)

    def put(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(
                {"message": "Event not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if event.organizer != request.user:
            return Response(
                {
                    "message": "You can edit only your own event."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(event,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

     
class TicketCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role != "organizer":
            return Response(
                {
                    "message": "Only organizer can view ticket categories."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        ticket_categories = TicketCategory.objects.filter(event__organizer=request.user)
        serializer = TicketCategorySerializer(ticket_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "organizer":
            return Response(
                {
                    "message": "Only organizer can create ticket category."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        print("Request data:", data)
        data["available_quantity"] = data["total_quantity"]
        
        event = Event.objects.filter(id=data["event"]).first()
        if event is None:
            return Response(
                {"message": "Event not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        

        if event.organizer != request.user:
            return Response(
                {"message": "You can create tickets only for your own events."},
                status=status.HTTP_403_FORBIDDEN
            )
        data["event_id"] = data["event"]
        
        serializer = TicketCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )