from django.db import models
from django.utils.text import slugify


class Program(models.Model):
    CATEGORY_CHOICES = [
        ("flr", "Landscape Restoration & Environment"),
        ("evangelism", "Evangelism & Biblical Education"),
        ("child_women", "Child Protection & Women Empowerment"),
        ("health", "Health, Nutrition & HIV Eradication"),
        ("agriculture", "Sustainable Agriculture & Cooperatives"),
        ("education", "Education & Vocational Training"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="flr")
    summary = models.TextField(help_text="Short summary displayed on cards and previews")
    description = models.TextField(help_text="Detailed description of the program and its impact")
    icon = models.CharField(max_length=50, default="tree", help_text="Icon identifier (e.g. tree, cross, shield, heart, sprouter)")
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="Fallback static image or CDN URL")
    target_beneficiaries = models.CharField(max_length=255, blank=True, default="Vulnerable households, women, youth")
    location = models.CharField(max_length=255, blank=True, default="Gatsibo, Rutsiro, Nyarugenge, Nyanza")
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Program / Activity"
        verbose_name_plural = "Programs & Activities"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def activity_points(self):
        sentences = [part.strip() for part in self.description.replace(";", ".").split(".") if part.strip()]
        return sentences[:4]


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ("flr", "Forest Landscape Restoration & Nurseries"),
        ("community", "Community Action & Cooperatives"),
        ("education", "Education & Graduations"),
        ("health", "Healthcare & Family Planning"),
        ("leadership", "Leadership & Field Visits"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="flr")
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="Fallback or local static photo URL")
    location = models.CharField(max_length=200, blank=True)
    date_taken = models.CharField(max_length=100, blank=True, default="2024-2026")
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class ImpactStat(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, default="check-circle")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Impact Statistic"
        verbose_name_plural = "Impact Statistics"

    def __str__(self):
        return f"{self.value} {self.label}"


class Partner(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, default="Strategic Partner")
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)
    logo_url = models.CharField(max_length=500, blank=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=200)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} — {self.position}"

    @property
    def initials(self):
        parts = [part for part in self.name.replace(".", " ").split() if part.isalpha()]
        if not parts:
            return "MP"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()


class Testimonial(models.Model):
    author = models.CharField(max_length=150)
    role = models.CharField(max_length=200)
    quote = models.TextField()
    location = models.CharField(max_length=150, default="Gatsibo District, Rwanda")
    image_url = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Farmer Testimonial"
        verbose_name_plural = "Farmer Testimonials"

    def __str__(self):
        return f"{self.author} - {self.location}"
