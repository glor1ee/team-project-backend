from django.core.validators import MinValueValidator
from django.db import models

from apps.locations.models import City


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    sku = models.CharField("SKU / article", max_length=50, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="equipment"
    )
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price_per_day = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to="equipment/", blank=True)
    available_cities = models.ManyToManyField(
        City, related_name="equipment", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-rating", "name"]
        verbose_name = "equipment"
        verbose_name_plural = "equipment"

    def __str__(self):
        return self.name


class EquipmentImage(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="equipment/gallery/")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.equipment.name} — image {self.order}"


class EquipmentSpec(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="specs"
    )
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label}: {self.value}"


class EquipmentIncludedItem(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="included_items"
    )
    name = models.CharField(max_length=150)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class EquipmentBenefit(models.Model):
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name="benefits"
    )
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text
