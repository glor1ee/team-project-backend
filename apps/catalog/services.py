"""Equipment availability — derived from bookings, never stored on Equipment.

catalog depends on bookings here (a one-off exception to the usual
direction): "чи доступна ця техніка" is fundamentally catalog's
concern, but the answer only exists in booking data. bookings.models
already depends on catalog.models (Equipment FK) — this doesn't create
an import cycle since it's a runtime service import, not a model one.
"""

from datetime import date, timedelta

from apps.bookings.models import Booking
from apps.catalog.models import Equipment


def equipment_availability(equipment: Equipment, on_date: date) -> dict:
    blocking = (
        Booking.objects.filter(
            equipment=equipment,
            status__in=Booking.ACTIVE_STATUSES,
            start_date__lte=on_date,
            end_date__gte=on_date,
        )
        .order_by("-end_date")
        .first()
    )
    if blocking is None:
        return {"status": "available", "available_from": None}
    return {"status": "booked", "available_from": blocking.end_date + timedelta(days=1)}


def annotate_availability(equipment_list, on_date: date) -> None:
    """Attach `.availability` to each Equipment instance with ONE query
    (instead of calling equipment_availability() per item — avoids N+1
    on the catalog list endpoint)."""
    equipment_ids = [item.pk for item in equipment_list]
    blocking_by_equipment = {}
    bookings = Booking.objects.filter(
        equipment_id__in=equipment_ids,
        status__in=Booking.ACTIVE_STATUSES,
        start_date__lte=on_date,
        end_date__gte=on_date,
    )
    for booking in bookings:
        blocking_by_equipment[booking.equipment_id] = booking

    for item in equipment_list:
        blocking = blocking_by_equipment.get(item.pk)
        if blocking is None:
            item.availability = {"status": "available", "available_from": None}
        else:
            item.availability = {
                "status": "booked",
                "available_from": blocking.end_date + timedelta(days=1),
            }


def related_equipment(equipment: Equipment, limit: int = 3) -> list[Equipment]:
    """Equipment for the "Інша техніка" carousel: same category first
    (best match), then top up with other active equipment if the
    category doesn't have enough on its own. Never includes `equipment`
    itself."""
    base_qs = (
        Equipment.objects.filter(is_active=True)
        .exclude(pk=equipment.pk)
        .select_related("category")
    )

    same_category = list(base_qs.filter(category=equipment.category)[:limit])
    if len(same_category) >= limit:
        return same_category

    remaining = limit - len(same_category)
    other_ids = [item.pk for item in same_category]
    fillers = list(
        base_qs.exclude(category=equipment.category).exclude(pk__in=other_ids)[
            :remaining
        ]
    )
    return same_category + fillers
