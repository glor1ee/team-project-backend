import datetime
from decimal import Decimal

import pytest

from apps.bookings.models import Booking
from apps.bookings.services import create_booking
from apps.catalog.models import Category, Equipment
from apps.locations.models import City

pytestmark = pytest.mark.django_db


def today_plus(days):
    return datetime.date.today() + datetime.timedelta(days=days)


@pytest.fixture
def city():
    return City.objects.create(name="Луцьк", slug="lutsk", is_default=True)


@pytest.fixture
def equipment(city):
    category = Category.objects.create(name="Пилососи", slug="vacuum-cleaners")
    eq = Equipment.objects.create(
        name="Karcher Puzzi 8/1", slug="karcher-puzzi-8-1", sku="PUZZI-8-1",
        category=category, price_per_day=Decimal("650.00"),
    )
    eq.available_cities.add(city)
    return eq


@pytest.fixture
def booking(equipment, city):
    return create_booking(
        equipment=equipment, city=city,
        customer_name="Іван", customer_phone="+380501234567",
        start_date=today_plus(5), end_date=today_plus(7),
        delivery_method=Booking.DeliveryMethod.PICKUP,
        payment_method=Booking.PaymentMethod.CASH,
    )


def test_lookup_requires_phone(client):
    assert client.get("/api/bookings/").status_code == 400


def test_lookup_returns_only_matching_phone(client, booking, equipment, city):
    create_booking(
        equipment=equipment, city=city,
        customer_name="Петро", customer_phone="+380671112233",
        start_date=today_plus(10), end_date=today_plus(12),
        delivery_method=Booking.DeliveryMethod.PICKUP,
        payment_method=Booking.PaymentMethod.CASH,
    )
    response = client.get("/api/bookings/", {"phone": booking.customer_phone})
    data = response.json()
    assert len(data) == 1
    assert data[0]["number"] == booking.number


def test_cancel_happy_path(client, booking):
    response = client.post(
        f"/api/bookings/{booking.number}/cancel/",
        {"phone": booking.customer_phone},
        content_type="application/json",
    )
    assert response.status_code == 200
    booking.refresh_from_db()
    assert booking.status == Booking.Status.CANCELLED


def test_cancel_rejects_wrong_phone(client, booking):
    response = client.post(
        f"/api/bookings/{booking.number}/cancel/",
        {"phone": "+380000000000"},
        content_type="application/json",
    )
    assert response.status_code == 404


def test_cancel_rejects_already_started(client, equipment, city):
    started = create_booking(
        equipment=equipment, city=city,
        customer_name="Іван", customer_phone="+380501234567",
        start_date=today_plus(1), end_date=today_plus(3),
        delivery_method=Booking.DeliveryMethod.PICKUP,
        payment_method=Booking.PaymentMethod.CASH,
    )
    started.start_date = datetime.date.today()
    started.save(update_fields=["start_date"])

    response = client.post(
        f"/api/bookings/{started.number}/cancel/",
        {"phone": started.customer_phone},
        content_type="application/json",
    )
    assert response.status_code == 400


def test_cancel_rejects_already_cancelled(client, booking):
    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=["status"])

    response = client.post(
        f"/api/bookings/{booking.number}/cancel/",
        {"phone": booking.customer_phone},
        content_type="application/json",
    )
    assert response.status_code == 400
