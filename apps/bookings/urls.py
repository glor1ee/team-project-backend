"""Bookings API routes."""

from django.urls import path

from apps.bookings.views import BookingCreateView, BookingQuoteView

app_name = "bookings"

urlpatterns = [
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/quote/", BookingQuoteView.as_view(), name="booking-quote"),
]
