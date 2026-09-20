from rest_framework import serializers

from apps.content.models import (
    AboutFeature,
    AboutSection,
    HeroSection,
    RentalStep,
    RentalTerm,
    SiteSettings,
)


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ("title", "subtitle", "cta_label", "cta_url", "background_image")


class AboutFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutFeature
        fields = ("icon", "text")


class AboutSectionSerializer(serializers.ModelSerializer):
    features = AboutFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = AboutSection
        fields = ("title", "description", "features")


class RentalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalStep
        fields = ("order", "icon", "title", "description")


class RentalTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalTerm
        fields = ("order", "icon", "title", "description")


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = (
            "company_name",
            "bank_name",
            "iban",
            "recipient_name",
            "edrpou",
            "transfer_note",
        )
