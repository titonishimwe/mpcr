from django.contrib import admin
from .models import Program, GalleryImage, ContactMessage, ImpactStat, Partner, Testimonial

# Customize Admin Site Branding
admin.site.site_header = "MPCR Administration - Movement for Christ in Rwanda"
admin.site.site_title = "MPCR Portal"
admin.site.index_title = "NGO Content & Communications Management"


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "is_featured", "order", "created_at"]
    list_filter = ["category", "is_featured"]
    search_fields = ["title", "summary", "description", "location"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_featured", "order"]
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "category", "order", "is_featured")
        }),
        ("Content & Details", {
            "fields": ("summary", "description", "target_beneficiaries", "location")
        }),
        ("Visuals", {
            "fields": ("icon", "image", "image_url")
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "location", "date_taken", "is_featured", "order", "created_at"]
    list_filter = ["category", "is_featured"]
    search_fields = ["title", "caption", "location"]
    list_editable = ["is_featured", "order"]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "subject", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "phone", "subject", "message"]
    readonly_fields = ["name", "email", "phone", "subject", "message", "created_at"]
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ["value", "label", "description", "icon", "order"]
    list_editable = ["order"]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "website", "order"]
    search_fields = ["name", "category"]
    list_editable = ["order"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author", "role", "location", "order"]
    search_fields = ["author", "quote", "location"]
    list_editable = ["order"]
