from django.db import transaction
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from events.models import TicketCategory
from .models import Booking, Payment
from .serializers import BookingSerializer


class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings,many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "attendee":
            return Response(
                {
                    "message": "Only attendee can book tickets."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        with transaction.atomic():
            try:
                ticket = TicketCategory.objects.select_for_update().get(
                    id=request.data["ticket_category"]
                )
            except TicketCategory.DoesNotExist:
                return Response(
                    {
                        "message": "Ticket category not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            quantity = int(request.data.get("quantity", 0))
            if quantity <= 0:
                return Response(
                    {
                        "message": "Quantity must be greater than 0."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            if ticket.available_quantity < quantity:
                return Response(
                    {
                        "message": "Tickets are not available."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            total = ticket.price * quantity
            ticket.available_quantity -= quantity
            ticket.save()
            booking = Booking.objects.create(
                user=request.user,
                event=ticket.event,
                ticket_category=ticket,
                quantity=quantity,
                total_amount=total,
                status="Pending"
            )
        serializer = BookingSerializer(booking)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
        

class OrganizerBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "organizer":
            return Response(
                {
                    "message": "Only organizer can view bookings."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        bookings = Booking.objects.filter(event__organizer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)    

    
class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            booking = Booking.objects.get(
                id=request.data["booking_id"],
                user=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Booking not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.status == "Confirmed":
            return Response(
                {
                    "message": "Payment already completed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
            
        payment_status = request.data["status"]
        
        if payment_status == "Failed":
            Payment.objects.create(booking=booking, status="Failed")
            booking.status = "Failed"
            booking.save()
            return Response(
                {
                    "message": "Payment Failed. You can retry."
                }
            )
        
        with transaction.atomic():
            if payment_status == "Success":
                
                ticket_category_id = booking.ticket_category.id

                if not ticket_category_id:
                    return Response(
                        {
                            "message": "ticket_category is required."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                try:
                    ticket = TicketCategory.objects.select_for_update().get(
                        id=ticket_category_id
                    )
                except TicketCategory.DoesNotExist:
                    return Response(
                        {
                            "message": "Ticket category not found."
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
                                  
                if ticket.available_quantity < booking.quantity:
                    return Response(
                        {
                            "message": "Tickets are sold out."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                ticket.available_quantity -= booking.quantity
                ticket.save()
                booking.status = "Confirmed"
                booking.ticket_code = (
                    "TKT-" +
                    uuid.uuid4().hex[:8].upper()
                )
                booking.save()
                Payment.objects.create(booking=booking, status="Success")
                return Response(
                    {
                        "message": "Payment Successful",
                        "ticket_code": booking.ticket_code
                    }
                )