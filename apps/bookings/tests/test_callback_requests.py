import pytest

from apps.bookings.models import CallbackRequest
from apps.catalog.models import Category, Equipment

pytestmark = pytest.mark.django_db


def test_create_callback_request_minimal(client):
    response = client.post(
        "/api/callback-requests/",
        {"phone": "+380501234567"},
        content_type="application/json",
    )
    assert response.status_code == 201
    request = CallbackRequest.objects.get()
    assert request.is_processed is False
    assert request.equipment is None


def test_create_callback_request_with_equipment_and_dates(client):
    category = Category.objects.create(name="Пилососи", slug="vacuum-cleaners")
    equipment = Equipment.objects.create(
        name="Karcher Puzzi 8/1",
        slug="karcher-puzzi-8-1",
        sku="PUZZI-8-1",
        category=category,
        price_per_day="650.00",
    )
    response = client.post(
        "/api/callback-requests/",
        {
            "phone": "+380501234567",
            "equipment": equipment.slug,
            "start_date": "2026-10-01",
            "end_date": "2026-10-03",
        },
        content_type="application/json",
    )
    assert response.status_code == 201
    assert CallbackRequest.objects.get().equipment == equipment


def test_phone_is_required(client):
    response = client.post(
        "/api/callback-requests/", {}, content_type="application/json"
    )
    assert response.status_code == 400
    assert "phone" in response.json()
