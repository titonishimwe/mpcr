from django.conf import settings
from django.db import models
from django.utils.text import slugify


CONTENT_CATEGORY_CHOICES = [
    ("evangelism", "Evangelism"),
    ("social", "Social (well being)"),
    ("economic", "Economic"),
    ("development", "Development"),
]


class Program(models.Model):
    CATEGORY_CHOICES = CONTENT_CATEGORY_CHOICES

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="evangelism")
    summary = models.TextField(help_text="Short summary displayed on cards and previews")
    description = models.TextField(help_text="Detailed description of the program and its impact")
    icon = models.CharField(max_length=50, default="tree", help_text="Icon identifier (e.g. tree, cross, shield, heart, sprouter)")
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="Fallback static image or CDN URL")
    target_beneficiaries = models.CharField(max_length=255, blank=True, default="Vulnerable households, women, youth")
    location = models.CharField(max_length=255, blank=True, default="Gatsibo, Rutsiro, Nyarugenge, Nyanza")
    is_featured = models.BooleanField(default=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Unpublished programs stay in the dashboard but are hidden from the public site.",
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Program / Activity"
        verbose_name_plural = "Programs & Activities"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "program"
            slug = base
            counter = 2
            while Program.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def activity_points(self):
        raw = (self.description or "").strip()
        if not raw:
            return []
        if "\n" in raw:
            points = [part.strip(" -\u2022\t") for part in raw.splitlines() if part.strip()]
        elif ";" in raw:
            points = [part.strip() for part in raw.split(";") if part.strip()]
        else:
            points = [part.strip() for part in raw.replace(";", ".").split(".") if part.strip()]
        return points[:6]


class GalleryImage(models.Model):
    CATEGORY_CHOICES = CONTENT_CATEGORY_CHOICES

    title = models.CharField(max_length=200, blank=True, default="")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="evangelism")
    caption = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, default="", help_text="Fallback or local static photo URL")
    location = models.CharField(max_length=200, blank=True, default="")
    date_taken = models.CharField(max_length=100, blank=True, default="")
    is_featured = models.BooleanField(default=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Unpublished photos stay in the dashboard but are hidden from the public site.",
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Gallery Photo"
        verbose_name_plural = "Gallery Photos"

    def __str__(self):
        return self.title.strip() or f"Gallery photo #{self.pk or 'new'}"


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
    is_published = models.BooleanField(
        default=True,
        help_text="Unpublished stats stay in the dashboard but are hidden from the public site.",
    )
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
    is_published = models.BooleanField(
        default=True,
        help_text="Unpublished partners stay in the dashboard but are hidden from the public site.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name

    @property
    def mark(self):
        short = (self.category or "").strip()
        if short and len(short) <= 6 and " " not in short:
            return short.upper()
        parts = [part for part in self.name.replace("(", " ").replace(")", " ").split() if part[:1].isalpha()]
        if not parts:
            return "MP"
        if len(parts) == 1:
            return parts[0][:3].upper()
        return "".join(part[0] for part in parts[:3]).upper()


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=200)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive members stay in the dashboard but are hidden from the public site.",
    )

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
    is_published = models.BooleanField(
        default=True,
        help_text="Unpublished testimonials stay in the dashboard but are hidden from the public site.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Farmer Testimonial"
        verbose_name_plural = "Farmer Testimonials"

    def __str__(self):
        return f"{self.author} - {self.location}"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account_profile",
    )
    pending_email = models.EmailField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_username()


class AccountActivity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account_activities",
    )
    action = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Account activity"
        verbose_name_plural = "Account activity"

    def __str__(self):
        return f"{self.user} — {self.action}"


class SiteSettings(models.Model):
    org_name = models.CharField(max_length=200, default="Movement for Christ in Rwanda (MPCR)")
    org_name_fr = models.CharField(max_length=200, blank=True, default="Mouvement Pour Christ au Rwanda")
    footer_about = models.TextField(blank=True)
    legal_badge = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    postal_box = models.CharField(max_length=120, blank=True)
    phone_primary = models.CharField(max_length=40, blank=True)
    phone_primary_raw = models.CharField(max_length=40, blank=True)
    phone_secondary = models.CharField(max_length=40, blank=True)
    phone_secondary_raw = models.CharField(max_length=40, blank=True)
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=40, blank=True)
    whatsapp_message = models.CharField(max_length=255, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    focus_items = models.TextField(blank=True, help_text="One focus item per line")
    footer_copyright = models.CharField(max_length=255, blank=True)
    footer_tagline = models.CharField(max_length=255, blank=True)
    social_handle = models.CharField(max_length=80, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def focus_list(self):
        return [line.strip() for line in self.focus_items.splitlines() if line.strip()]

    @property
    def whatsapp_url(self):
        number = "".join(ch for ch in (self.whatsapp_number or "") if ch.isdigit())
        if not number:
            return "#"
        from urllib.parse import quote

        message = quote(self.whatsapp_message or "")
        return f"https://wa.me/{number}?text={message}" if message else f"https://wa.me/{number}"


class PageSection(models.Model):
    FIELD_TEXT = "text"
    FIELD_TEXTAREA = "textarea"
    FIELD_LIST = "list"
    FIELD_IMAGE = "image"
    FIELD_CHOICES = [
        (FIELD_TEXT, "Short text"),
        (FIELD_TEXTAREA, "Long text"),
        (FIELD_LIST, "List"),
        (FIELD_IMAGE, "Image"),
    ]
    PAGE_CHOICES = [
        ("home", "Home"),
        ("about", "About"),
        ("programs", "Programs"),
        ("gallery", "Gallery"),
        ("contact", "Contact"),
    ]

    page = models.CharField(max_length=40, choices=PAGE_CHOICES, db_index=True)
    key = models.SlugField(max_length=80)
    label = models.CharField(max_length=120)
    field_type = models.CharField(max_length=20, choices=FIELD_CHOICES, default=FIELD_TEXT)
    value = models.TextField(blank=True)
    image = models.ImageField(upload_to="cms/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, help_text="Static path or external URL fallback")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["page", "order", "key"]
        unique_together = [("page", "key")]
        verbose_name = "Page section"
        verbose_name_plural = "Page sections"

    def __str__(self):
        return f"{self.page}:{self.key}"

    @property
    def lines(self):
        return [line.strip() for line in self.value.splitlines() if line.strip()]

    @property
    def pairs(self):
        items = []
        for line in self.lines:
            if "|" in line:
                title, detail = line.split("|", 1)
                items.append((title.strip(), detail.strip()))
            else:
                items.append((line, ""))
        return items

    @property
    def media_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ""


class HeroSlide(models.Model):
    title = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to="hero/", blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive slides stay in the dashboard but are hidden from the public site.",
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Hero slide"
        verbose_name_plural = "Hero slides"

    def __str__(self):
        return self.title or f"Slide {self.order}"

    @property
    def media_url(self):
        if self.image:
            return self.image.url
        return self.image_url or ""


class EmptySection:
    value = ""
    image = None
    image_url = ""
    lines = []
    pairs = []
    media_url = ""


class SectionMap(dict):
    def __missing__(self, key):
        return EmptySection()

    def text(self, key, default=""):
        section = self.get(key)
        if section and getattr(section, "value", ""):
            return section.value
        return default

    def lines(self, key):
        section = self.get(key)
        return section.lines if section and hasattr(section, "lines") else []

    def pairs(self, key):
        section = self.get(key)
        return section.pairs if section and hasattr(section, "pairs") else []

    def media(self, key, default=""):
        section = self.get(key)
        url = getattr(section, "media_url", "") if section else ""
        return url or default


def get_page_sections(page):
    queryset = PageSection.objects.filter(page=page)
    if not queryset.exists():
        ensure_cms_defaults()
        queryset = PageSection.objects.filter(page=page)
    return SectionMap({section.key: section for section in queryset})


def ensure_cms_defaults():
    from .cms_defaults import HERO_SLIDE_DEFAULTS, SECTION_DEFAULTS, SITE_SETTINGS_DEFAULTS

    settings_obj = SiteSettings.load()
    for field, value in SITE_SETTINGS_DEFAULTS.items():
        if not getattr(settings_obj, field):
            setattr(settings_obj, field, value)
    settings_obj.save()

    existing = {(s.page, s.key) for s in PageSection.objects.all().only("page", "key")}
    to_create = []
    for page, key, label, field_type, value, order in SECTION_DEFAULTS:
        if (page, key) in existing:
            continue
        section = PageSection(
            page=page,
            key=key,
            label=label,
            field_type=field_type,
            order=order,
        )
        if field_type == PageSection.FIELD_IMAGE:
            section.image_url = value
        else:
            section.value = value
        to_create.append(section)
    if to_create:
        PageSection.objects.bulk_create(to_create)

    if not HeroSlide.objects.exists():
        HeroSlide.objects.bulk_create(
            [
                HeroSlide(title=f"Slide {index}", image_url=path, order=index, is_active=True)
                for index, path in enumerate(HERO_SLIDE_DEFAULTS, start=1)
            ]
        )
