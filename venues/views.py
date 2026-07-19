from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Venue
from .serializers import VenueSerializer


class VenueListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role != "organizer":
            return Response(
                {
                    "message": "Only organizer can create venue."
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = VenueSerializer(data=request.data)
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