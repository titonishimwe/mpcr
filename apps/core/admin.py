from django.contrib import admin
from .models import (
    Program,
    GalleryImage,
    ContactMessage,
    ImpactStat,
    Partner,
    TeamMember,
    Testimonial,
    SiteSettings,
    PageSection,
    HeroSlide,
)

# Customize Admin Site Branding
admin.site.site_header = "MPCR Administration - Movement for Christ in Rwanda"
admin.site.site_title = "MPCR Portal"
admin.site.index_title = "NGO Content & Communications Management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["org_name", "email_primary", "phone_primary", "updated_at"]


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ["page", "label", "key", "field_type", "order"]
    list_filter = ["page", "field_type"]
    search_fields = ["key", "label", "value"]
    list_editable = ["order"]


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active"]
    list_editable = ["order", "is_active"]


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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "phone", "email", "order", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "position", "phone", "email"]
    list_editable = ["order", "is_active"]
    fields = ["name", "position", "phone", "email", "photo", "order", "is_active"]


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
