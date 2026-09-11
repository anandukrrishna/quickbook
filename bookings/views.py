from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer
from .services import create_booking, cancel_booking


class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        event_id = request.data.get('event')
        number_of_tickets = request.data.get(
            'number_of_tickets'
        )

        if event_id is None:
            return Response(
                {"event": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if number_of_tickets is None:
            return Response(
                {
                    "number_of_tickets":
                    "This field is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            number_of_tickets = int(number_of_tickets)
        except (TypeError, ValueError):
            return Response(
                {
                    "number_of_tickets":
                    "A valid integer is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = create_booking(
            user=request.user,
            event_id=event_id,
            number_of_tickets=number_of_tickets
        )

        serializer = BookingSerializer(booking)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(
                id=booking_id,
                user=request.user
            )

        except Booking.DoesNotExist:
            return Response(
                {"detail": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        booking = cancel_booking(booking)

        serializer = BookingSerializer(booking)

        return Response(serializer.data)