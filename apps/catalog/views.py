from rest_framework import viewsets

from apps.catalog.filters import EquipmentFilter
from apps.catalog.models import Category, Equipment
from apps.catalog.pagination import EquipmentPagination
from apps.catalog.serializers import (
    CategorySerializer,
    EquipmentDetailSerializer,
    EquipmentListSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None


class EquipmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Equipment.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "images", "specs", "included_items", "benefits", "available_cities"
        )
    )
    lookup_field = "slug"
    pagination_class = EquipmentPagination
    filterset_class = EquipmentFilter
    search_fields = ("name", "sku", "short_description")
    ordering_fields = ("rating", "price_per_day")

    def get_serializer_class(self):
        if self.action == "list":
            return EquipmentListSerializer
        return EquipmentDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        exclude_slug = self.request.query_params.get("exclude")
        if exclude_slug:
            queryset = queryset.exclude(slug=exclude_slug)
        return queryset
