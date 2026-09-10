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
            "icon",
            "image",
            "image_url",
            "is_featured",
            "order",
        ]
        help_texts = {
            "slug": "Leave blank to generate from the title.",
            "image": "Upload a photo. Used on the home and programs pages.",
            "image_url": "Optional fallback image address if no file is uploaded.",
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
            "order",
        ]
        help_texts = {
            "image": "Upload the field photo shown in the gallery.",
            "is_featured": "Featured photos also appear on the home page.",
        }


class TeamMemberForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "position", "phone", "email", "photo", "order", "is_active"]
        help_texts = {
            "photo": "Profile photo shown on the team slider.",
            "is_active": "Inactive members are hidden from the public site.",
        }


class PartnerForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name", "category", "logo", "logo_url", "website", "order"]
        help_texts = {
            "category": "Short mark used as the thumbnail when no logo is uploaded (for example WRI or AFF).",
            "logo": "Upload a logo when one is available. Otherwise a thumbnail is shown.",
        }


class ImpactStatForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = ImpactStat
        fields = ["value", "label", "description", "icon", "order"]


class TestimonialForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["author", "role", "quote", "location", "image_url", "order"]


