from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.content.models import (
    AboutSection,
    HeroSection,
    RentalStep,
    RentalTerm,
    SiteSettings,
)
from apps.content.serializers import (
    AboutSectionSerializer,
    HeroSectionSerializer,
    RentalStepSerializer,
    RentalTermSerializer,
    SiteSettingsSerializer,
)


class HeroSectionView(RetrieveAPIView):
    serializer_class = HeroSectionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return HeroSection.load()


class AboutSectionView(RetrieveAPIView):
    serializer_class = AboutSectionSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return AboutSection.load()


class SiteSettingsView(RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return SiteSettings.load()


class RentalStepListView(ListAPIView):
    queryset = RentalStep.objects.filter(is_active=True)
    serializer_class = RentalStepSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RentalTermListView(ListAPIView):
    queryset = RentalTerm.objects.filter(is_active=True)
    serializer_class = RentalTermSerializer
    permission_classes = [AllowAny]
    pagination_class = None
