from rest_framework import serializers

from apps.catalog.models import (
    Category,
    Equipment,
    EquipmentBadge,
    EquipmentBenefit,
    EquipmentImage,
    EquipmentIncludedItem,
    EquipmentSpec,
    EquipmentUseCase,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class AvailabilitySerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["available", "booked"])
    available_from = serializers.DateField(allow_null=True)


class EquipmentListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    availability = AvailabilitySerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "price_per_day",
            "rating",
            "main_image",
            "is_popular",
            "availability",
        )


class EquipmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentImage
        fields = ("id", "image", "order")


class EquipmentSpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentSpec
        fields = ("label", "value")


class EquipmentIncludedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentIncludedItem
        fields = ("name",)


class EquipmentBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentBenefit
        fields = ("text",)


class EquipmentBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentBadge
        fields = ("label",)


class EquipmentUseCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentUseCase
        fields = ("text",)


class EquipmentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    availability = AvailabilitySerializer(read_only=True)
    images = EquipmentImageSerializer(many=True, read_only=True)
    specs = EquipmentSpecSerializer(many=True, read_only=True)
    included_items = EquipmentIncludedItemSerializer(many=True, read_only=True)
    benefits = EquipmentBenefitSerializer(many=True, read_only=True)
    badges = EquipmentBadgeSerializer(many=True, read_only=True)
    suitable_for = EquipmentUseCaseSerializer(many=True, read_only=True)
    available_cities = serializers.SlugRelatedField(
        slug_field="slug", many=True, read_only=True
    )
    breadcrumbs = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields = (
            "id",
            "name",
            "slug",
            "sku",
            "category",
            "short_description",
            "description",
            "price_per_day",
            "rating",
            "main_image",
            "availability",
            "badges",
            "images",
            "specs",
            "included_items",
            "benefits",
            "suitable_for",
            "available_cities",
            "breadcrumbs",
        )

    def get_breadcrumbs(self, obj):
        return [
            {"label": "Головна", "url": "/"},
            {"label": "Каталог", "url": "/catalog"},
            {
                "label": obj.category.name,
                "url": f"/catalog?category={obj.category.slug}",
            },
            {"label": obj.name, "url": None},
        ]
