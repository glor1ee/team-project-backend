from django.db import models

from apps.catalog.models import Equipment
from apps.locations.models import City


class Booking(models.Model):
    class DeliveryMethod(models.TextChoices):
        PICKUP = "pickup", "Самовивіз"
        COURIER = "courier", "Кур'єрська доставка"

    class PaymentMethod(models.TextChoices):
        CASH = "cash", "Готівка"
        TRANSFER = "transfer", "Безготівковий переказ"

    class Status(models.TextChoices):
        PENDING = "pending", "Очікує підтвердження"
        CONFIRMED = "confirmed", "Підтверджено"
        ACTIVE = "active", "Триває"
        COMPLETED = "completed", "Завершено"
        CANCELLED = "cancelled", "Скасовано"

    ACTIVE_STATUSES = (Status.PENDING, Status.CONFIRMED, Status.ACTIVE)

    number = models.CharField(max_length=10, unique=True, editable=False)
    equipment = models.ForeignKey(
        Equipment, on_delete=models.PROTECT, related_name="bookings"
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="bookings")

    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=20)

    start_date = models.DateField()
    end_date = models.DateField()

    delivery_method = models.CharField(max_length=10, choices=DeliveryMethod.choices)
    delivery_address = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    comment = models.TextField(blank=True)

    # Frozen at creation — never recomputed from live equipment prices.
    rental_days = models.PositiveSmallIntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.number


class CallbackRequest(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="callback_requests",
    )
    phone = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "оброблено" if self.is_processed else "нова"
        return f"{self.phone} ({status})"
