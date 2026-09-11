from django.db import transaction
from rest_framework.exceptions import ValidationError

from events.models import Event
from .models import Booking


@transaction.atomic
def create_booking(user, event_id, number_of_tickets):

    if number_of_tickets <= 0:
        raise ValidationError({
            "number_of_tickets":
            "Number of tickets must be greater than zero."
        })

    try:
        event = Event.objects.select_for_update().get(
            id=event_id
        )

    except Event.DoesNotExist:
        raise ValidationError({
            "event": "Event not found."
        })

    if event.available_seats < number_of_tickets:
        raise ValidationError({
            "number_of_tickets":
            "Not enough seats available."
        })

    event.available_seats -= number_of_tickets

    event.save(
        update_fields=['available_seats']
    )

    booking = Booking.objects.create(
        user=user,
        event=event,
        number_of_tickets=number_of_tickets
    )

    return booking


@transaction.atomic
def cancel_booking(booking):

    booking = Booking.objects.select_for_update().get(
        id=booking.id
    )

    if booking.status == 'CANCELLED':
        raise ValidationError({
            "detail": "Booking is already cancelled."
        })

    event = Event.objects.select_for_update().get(
        id=booking.event_id
    )

    event.available_seats += booking.number_of_tickets

    event.save(
        update_fields=['available_seats']
    )

    booking.status = 'CANCELLED'

    booking.save(
        update_fields=['status']
    )

    return booking