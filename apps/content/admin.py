from django.contrib import admin

from apps.content.models import (
    AboutFeature,
    AboutSection,
    HeroSection,
    RentalStep,
    RentalTerm,
    SiteSettings,
)


class SingletonAdmin(admin.ModelAdmin):
    """Base for models that must only ever have one row."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ("title", "cta_label", "updated_at")


class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 1


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    list_display = ("title", "updated_at")
    inlines = [AboutFeatureInline]


class OrderedContentAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_display_links = ("title",)


@admin.register(RentalStep)
class RentalStepAdmin(OrderedContentAdmin):
    pass


@admin.register(RentalTerm)
class RentalTermAdmin(OrderedContentAdmin):
    pass


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ("company_name", "iban", "updated_at")
