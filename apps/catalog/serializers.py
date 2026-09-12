from rest_framework import serializers

from apps.catalog.models import (
    Category,
    Equipment,
    EquipmentBenefit,
    EquipmentImage,
    EquipmentIncludedItem,
    EquipmentSpec,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class EquipmentListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = (
            "id", "name", "slug", "category",
            "price_per_day", "rating", "main_image", "is_popular",
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


class EquipmentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = EquipmentImageSerializer(many=True, read_only=True)
    specs = EquipmentSpecSerializer(many=True, read_only=True)
    included_items = EquipmentIncludedItemSerializer(many=True, read_only=True)
    benefits = EquipmentBenefitSerializer(many=True, read_only=True)
    available_cities = serializers.SlugRelatedField(
        slug_field="slug", many=True, read_only=True
    )

    class Meta:
        model = Equipment
        fields = (
            "id", "name", "slug", "sku", "category",
            "short_description", "description",
            "price_per_day", "rating", "main_image",
            "images", "specs", "included_items", "benefits",
            "available_cities",
        )
