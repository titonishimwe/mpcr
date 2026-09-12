from django import forms

from .models import GalleryImage, ImpactStat, Partner, Program, TeamMember, Testimonial


class DashboardFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "dash-check")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-input")
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "form-textarea")
                widget.attrs.setdefault("rows", 4)
            else:
                widget.attrs.setdefault("class", "form-input")


class ProgramForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            "title",
            "slug",
            "category",
            "summary",
            "description",
            "target_beneficiaries",
            "location",
            "image",
            "image_url",
            "is_featured",
            "is_published",
            "order",
        ]
        help_texts = {
            "slug": "Leave blank to generate from the title.",
            "image": "Upload a photo. Used on the home and programs pages.",
            "image_url": "Optional fallback image address if no file is uploaded.",
            "location": "Shown on the program detail page.",
            "target_beneficiaries": "Shown on the program detail page.",
            "is_featured": "Featured programs also appear on the home page.",
            "is_published": "Uncheck to hide from the public site without deleting.",
        }


class GalleryImageForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = [
            "title",
            "category",
            "caption",
            "image",
            "image_url",
            "location",
            "date_taken",
            "is_featured",
            "is_published",
            "order",
        ]
        help_texts = {
            "title": "Optional. Leave blank if the photo needs no title.",
            "caption": "Optional description for the photo.",
            "image": "Upload the field photo shown in the gallery.",
            "image_url": "Optional fallback image path or URL if no file is uploaded.",
            "location": "Optional.",
            "date_taken": "Optional.",
            "is_featured": "Featured photos also appear on the home page.",
            "is_published": "Uncheck to hide from the public site without deleting.",
            "order": "Optional. Lower numbers appear first.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("title", "caption", "image", "image_url", "location", "date_taken", "order"):
            if name in self.fields:
                self.fields[name].required = False

    def clean(self):
        cleaned = super().clean()
        image = cleaned.get("image") or getattr(self.instance, "image", None)
        image_url = (cleaned.get("image_url") or "").strip()
        if not image and not image_url:
            raise forms.ValidationError("Add an image file or an image URL.")
        if cleaned.get("order") is None:
            cleaned["order"] = 0
        return cleaned


class TeamMemberForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "position", "phone", "email", "photo", "order", "is_active"]
        labels = {"is_active": "Visible on site"}
        help_texts = {
            "photo": "Profile photo shown on the team slider.",
            "is_active": "Uncheck to hide from the public site without deleting.",
        }


class PartnerForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name", "category", "logo", "logo_url", "website", "is_published", "order"]
        help_texts = {
            "category": "Short mark used as the thumbnail when no logo is uploaded (for example WRI or AFF).",
            "logo": "Upload a logo when one is available. Otherwise a thumbnail is shown.",
            "is_published": "Uncheck to hide from the public site without deleting.",
        }


class ImpactStatForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = ImpactStat
        fields = ["value", "label", "description", "icon", "is_published", "order"]
        help_texts = {
            "is_published": "Uncheck to hide from the public site without deleting.",
        }


class TestimonialForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["author", "role", "quote", "location", "image_url", "is_published", "order"]
        help_texts = {
            "is_published": "Uncheck to hide from the public site without deleting.",
        }
