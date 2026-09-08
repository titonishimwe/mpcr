from io import BytesIO

from django.db import migrations, models


MEMBERS = [
    {
        "name": "Dr. Silas KANYABIGEGA",
        "position": "Founder and International President",
        "phone": "+1 (937) 559-5862",
        "email": "kanyabigegasilas@gmail.com",
        "order": 1,
        "initials": "SK",
        "fill": (27, 122, 58),
    },
    {
        "name": "Eraste NDAYISENGA",
        "position": "Legal Representative",
        "phone": "(+250) 788 812 075",
        "email": "info@mouvementpourchriste.org",
        "order": 2,
        "initials": "EN",
        "fill": (21, 101, 47),
    },
    {
        "name": "Elisée MUNYEMANA",
        "position": "Committee Head",
        "phone": "",
        "email": "",
        "order": 3,
        "initials": "EM",
        "fill": (46, 140, 74),
    },
]


def _profile_png(initials, fill):
    from PIL import Image, ImageDraw, ImageFont

    size = 400
    image = Image.new("RGB", (size, size), fill)
    draw = ImageDraw.Draw(image)
    draw.ellipse((18, 18, size - 18, size - 18), outline=(212, 168, 67), width=14)

    font = None
    for path in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        try:
            font = ImageFont.truetype(path, 132)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()

    box = draw.textbbox((0, 0), initials, font=font)
    text_w = box[2] - box[0]
    text_h = box[3] - box[1]
    draw.text(
        ((size - text_w) / 2, (size - text_h) / 2 - 8),
        initials,
        fill=(255, 255, 255),
        font=font,
    )

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def seed_members(apps, schema_editor):
    from django.core.files.base import ContentFile

    TeamMember = apps.get_model("core", "TeamMember")
    for member in MEMBERS:
        person, _created = TeamMember.objects.get_or_create(
            name=member["name"],
            defaults={
                "position": member["position"],
                "phone": member["phone"],
                "email": member["email"],
                "order": member["order"],
                "is_active": True,
            },
        )
        person.position = member["position"]
        person.phone = member["phone"]
        person.email = member["email"]
        person.order = member["order"]
        person.is_active = True
        if not person.photo:
            person.photo.save(
                f"{member['initials'].lower()}-profile.png",
                ContentFile(_profile_png(member["initials"], member["fill"])),
                save=False,
            )
        person.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_teammember"),
    ]

    operations = [
        migrations.AddField(
            model_name="teammember",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="team/"),
        ),
        migrations.RunPython(seed_members, migrations.RunPython.noop),
    ]
