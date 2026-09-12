import django_filters

from apps.catalog.models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method="filter_category")
    city = django_filters.CharFilter(method="filter_city")
    price_min = django_filters.NumberFilter(field_name="price_per_day", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price_per_day", lookup_expr="lte")
    is_popular = django_filters.BooleanFilter()

    class Meta:
        model = Equipment
        fields = []

    def filter_category(self, queryset, name, value):
        slugs = [s.strip() for s in value.split(",") if s.strip()]
        return queryset.filter(category__slug__in=slugs)

    def filter_city(self, queryset, name, value):
        slugs = [s.strip() for s in value.split(",") if s.strip()]
        return queryset.filter(available_cities__slug__in=slugs).distinct()
