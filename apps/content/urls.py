"""Content API routes — editable homepage sections."""

from django.urls import path

from apps.content.views import (
    AboutSectionView,
    HeroSectionView,
    RentalStepListView,
    RentalTermListView,
    SiteSettingsView,
)

app_name = "content"

urlpatterns = [
    path("content/hero/", HeroSectionView.as_view(), name="hero"),
    path("content/about/", AboutSectionView.as_view(), name="about"),
    path("content/rental-steps/", RentalStepListView.as_view(), name="rental-steps"),
    path("content/rental-terms/", RentalTermListView.as_view(), name="rental-terms"),
    path("content/settings/", SiteSettingsView.as_view(), name="settings"),
]
