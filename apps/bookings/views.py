from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bookings.serializers import (
    BookingCreateSerializer,
    BookingQuoteResponseSerializer,
    BookingQuoteSerializer,
    CallbackRequestSerializer,
)
from apps.bookings.services import quote_price
from apps.bookings.models import CallbackRequest


class BookingCreateView(APIView):
    permission_classes = [AllowAny]

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

class CallbackRequestCreateView(generics.CreateAPIView):
    queryset = CallbackRequest.objects.all()
    serializer_class = CallbackRequestSerializer
    permission_classes = [AllowAny]
