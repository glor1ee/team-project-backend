"""Bookings API routes."""

from django.urls import path

from apps.bookings.views import BookingCreateView, BookingQuoteView, CallbackRequestCreateView

app_name = "bookings"

urlpatterns = [
    path("bookings/", BookingCreateView.as_view(), name="booking-create"),
    path("bookings/quote/", BookingQuoteView.as_view(), name="booking-quote"),
    path("callback-requests/", CallbackRequestCreateView.as_view(), name="callback-request-create"),
]
