from django.urls import path
from .views import BookingListCreateView, BookingCancelView

urlpatterns = [
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
    path('<int:booking_id>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]