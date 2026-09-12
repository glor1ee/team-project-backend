from django.contrib import admin

from apps.catalog.models import (
    Category,
    Equipment,
    EquipmentBenefit,
    EquipmentImage,
    EquipmentIncludedItem,
    EquipmentSpec,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


class EquipmentImageInline(admin.TabularInline):
    model = EquipmentImage
    extra = 1


class EquipmentSpecInline(admin.TabularInline):
    model = EquipmentSpec
    extra = 1


class EquipmentIncludedItemInline(admin.TabularInline):
    model = EquipmentIncludedItem
    extra = 1


class EquipmentBenefitInline(admin.TabularInline):
    model = EquipmentBenefit
    extra = 1


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price_per_day", "rating", "is_popular", "is_active",
    )
    list_filter = ("category", "is_popular", "is_active", "available_cities")
    search_fields = ("name", "sku")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("available_cities",)
    inlines = [
        EquipmentImageInline,
        EquipmentSpecInline,
        EquipmentIncludedItemInline,
        EquipmentBenefitInline,
    ]