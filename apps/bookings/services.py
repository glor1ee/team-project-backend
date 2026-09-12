"""Booking business logic — pricing, availability and creation.

Concurrency: create_booking() takes a row lock on the Equipment being
booked (select_for_update) before checking for overlapping bookings.
This serialises concurrent booking attempts for the SAME equipment —
a plain overlap query on Booking cannot do that on its own, because a
SELECT ... FOR UPDATE on a query matching zero rows locks nothing.
"""

import random
import string
from datetime import date
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.bookings.models import Booking
from apps.catalog.models import Equipment

DELIVERY_FEE = Decimal("100.00")


class BookingError(Exception):
    """Base class for booking validation failures."""


class InvalidDateRangeError(BookingError):
    pass


class EquipmentNotInCityError(BookingError):
    pass


class EquipmentNotAvailableError(BookingError):
    pass


def generate_booking_number() -> str:
    for _ in range(10):
        candidate = "ER-" + "".join(random.choices(string.digits, k=5))
        if not Booking.objects.filter(number=candidate).exists():
            return candidate
    raise RuntimeError("Could not generate a unique booking number")


def calculate_rental_days(start_date: date, end_date: date) -> int:
    return (end_date - start_date).days + 1


def quote_price(
    *, equipment: Equipment, start_date: date, end_date: date, delivery_method: str
) -> dict:
    rental_days = calculate_rental_days(start_date, end_date)
    delivery_fee = (
        DELIVERY_FEE
        if delivery_method == Booking.DeliveryMethod.COURIER
        else Decimal("0")
    )
    total_price = equipment.price_per_day * rental_days + delivery_fee
    return {
        "rental_days": rental_days,
        "price_per_day": equipment.price_per_day,
        "delivery_fee": delivery_fee,
        "total_price": total_price,
    }


def assert_dates_valid(start_date: date, end_date: date) -> None:
    if end_date < start_date:
        raise InvalidDateRangeError("Дата завершення не може бути раніше дати початку.")
    if start_date < timezone.localdate():
        raise InvalidDateRangeError("Дата початку оренди не може бути в минулому.")


def assert_available(
    *, equipment: Equipment, city, start_date: date, end_date: date,
    exclude_booking_id=None,
) -> None:
    if not equipment.available_cities.filter(pk=city.pk).exists():
        raise EquipmentNotInCityError(f"«{equipment.name}» недоступна у місті {city.name}.")

    conflicts = Booking.objects.filter(
        equipment=equipment,
        status__in=Booking.ACTIVE_STATUSES,
        start_date__lte=end_date,
        end_date__gte=start_date,
    )
    if exclude_booking_id:
        conflicts = conflicts.exclude(pk=exclude_booking_id)
    if conflicts.exists():
        raise EquipmentNotAvailableError(f"«{equipment.name}» вже заброньована на обрані дати.")


@transaction.atomic
def create_booking(
    *, equipment: Equipment, city, customer_name: str, customer_phone: str,
    start_date: date, end_date: date, delivery_method: str, payment_method: str,
    delivery_address: str = "", comment: str = "",
) -> Booking:
    # Lock the equipment row so two concurrent requests for it serialise.
    equipment = Equipment.objects.select_for_update().get(pk=equipment.pk)

    assert_dates_valid(start_date, end_date)
    assert_available(
        equipment=equipment, city=city, start_date=start_date, end_date=end_date
    )
    pricing = quote_price(
        equipment=equipment,
        start_date=start_date,
        end_date=end_date,
        delivery_method=delivery_method,
    )

    return Booking.objects.create(
        number=generate_booking_number(),
        equipment=equipment,
        city=city,
        customer_name=customer_name,
        customer_phone=customer_phone,
        start_date=start_date,
        end_date=end_date,
        delivery_method=delivery_method,
        delivery_address=delivery_address,
        payment_method=payment_method,
        comment=comment,
        **pricing,
    )
