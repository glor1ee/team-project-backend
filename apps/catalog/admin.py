from django.contrib import admin
from django.utils.html import format_html

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
        "thumbnail",
        "name",
        "category",
        "price_per_day",
        "rating",
        "is_popular",
        "is_active",
    )
    list_display_links = ("thumbnail", "name")
    list_filter = ("category", "is_popular", "is_active", "available_cities")
    search_fields = ("name", "sku")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("available_cities",)
    readonly_fields = ("created_at", "preview")
    fieldsets = (
        (None, {"fields": ("name", "slug", "sku", "category")}),
        ("Опис", {"fields": ("short_description", "description")}),
        ("Ціна та рейтинг", {"fields": ("price_per_day", "rating")}),
        ("Показ на сайті", {"fields": ("is_popular", "is_active", "available_cities")}),
        ("Фото", {"fields": ("main_image", "preview")}),
        ("Службове", {"fields": ("created_at",)}),
    )
    inlines = [
        EquipmentImageInline,
        EquipmentSpecInline,
        EquipmentIncludedItemInline,
        EquipmentBenefitInline,
    ]

    @admin.display(description="Фото")
    def thumbnail(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="height:40px">', obj.main_image.url)
        return "—"

    @admin.display(description="Попередній перегляд")
    def preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="max-height:200px">', obj.main_image.url
            )
        return "Фото ще не завантажено"
