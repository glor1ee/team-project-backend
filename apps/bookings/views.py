from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookings.models import CallbackRequest
from apps.bookings.serializers import (
    BookingCancelSerializer,
    BookingCreateSerializer,
    BookingQuoteResponseSerializer,
    BookingQuoteSerializer,
    BookingSerializer,
    CallbackRequestSerializer,
)
from apps.bookings.services import (
    BookingNotCancellableError,
    BookingNotFoundError,
    cancel_booking,
    get_bookings_by_phone,
    quote_price,
)


class BookingListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        phone = request.query_params.get("phone")
        if not phone:
            return Response(
                {"phone": ["This query parameter is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        bookings = get_bookings_by_phone(phone)
        return Response(BookingSerializer(bookings, many=True).data)

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingQuoteView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BookingQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        pricing = quote_price(
            equipment=data["equipment"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            delivery_method=data["delivery_method"],
        )
        return Response(BookingQuoteResponseSerializer(pricing).data)


class BookingCancelView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, number):
        serializer = BookingCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            booking = cancel_booking(
                number=number, phone=serializer.validated_data["phone"]
            )
        except BookingNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except BookingNotCancellableError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(BookingSerializer(booking).data)


class CallbackRequestCreateView(generics.CreateAPIView):
    queryset = CallbackRequest.objects.all()
    serializer_class = CallbackRequestSerializer
    permission_classes = [AllowAny]
