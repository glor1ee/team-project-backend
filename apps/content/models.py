"""Editable content for the home page — no hardcoded copy on the frontend.

HeroSection, AboutSection and SiteSettings are singletons: save() forces
pk=1 so a second row can never be created (even from a shell or fixture),
and the admin additionally hides the "Add" button once a row exists
(see content/admin.py). load() returns the single row, creating a blank
one on first access so an empty database never 500s the API.
"""

from django.db import models


class HeroSection(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    subtitle = models.TextField(blank=True, default="")
    cta_label = models.CharField(max_length=60, blank=True, default="")
    cta_url = models.CharField(max_length=200, blank=True, default="")
    background_image = models.ImageField(upload_to="content/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "hero section"
        verbose_name_plural = "hero section"

    def __str__(self):
        return self.title or "Hero section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutSection(models.Model):
    title = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "about section"
        verbose_name_plural = "about section"

    def __str__(self):
        return self.title or "About section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutFeature(models.Model):
    about = models.ForeignKey(
        AboutSection, on_delete=models.CASCADE, related_name="features"
    )
    icon = models.CharField(max_length=50, blank=True)
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class RentalStep(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class RentalTerm(models.Model):
    order = models.PositiveSmallIntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    company_name = models.CharField(max_length=150, blank=True, default="")
    bank_name = models.CharField(max_length=150, blank=True, default="")
    iban = models.CharField(max_length=40, blank=True, default="")
    recipient_name = models.CharField(max_length=150, blank=True, default="")
    edrpou = models.CharField("ЄДРПОУ / ІПН", max_length=20, blank=True, default="")
    transfer_note = models.TextField(blank=True, default="")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "site settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
