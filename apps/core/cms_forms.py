from django import forms

from .dashboard_forms import DashboardFormMixin
from .models import HeroSlide, SiteSettings


class SiteSettingsForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "org_name",
            "org_name_fr",
            "footer_about",
            "legal_badge",
            "address_line_1",
            "address_line_2",
            "postal_box",
            "phone_primary",
            "phone_primary_raw",
            "phone_secondary",
            "phone_secondary_raw",
            "email_primary",
            "email_secondary",
            "whatsapp_number",
            "whatsapp_message",
            "facebook_url",
            "instagram_url",
            "twitter_url",
            "social_handle",
            "focus_items",
            "footer_copyright",
            "footer_tagline",
        ]
        help_texts = {
            "phone_primary_raw": "Digits used for tel: links, e.g. +250788812075",
            "whatsapp_number": "Digits only country code included, e.g. 250788812075",
            "focus_items": "One focus item per line for the footer.",
        }


class HeroSlideForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = ["title", "image", "image_url", "order", "is_active"]
        labels = {"is_active": "Visible on site"}
        help_texts = {
            "image": "Upload a hero background image.",
            "image_url": "Optional static path or URL if no upload is used.",
            "is_active": "Uncheck to hide from the public site without deleting.",
        }
