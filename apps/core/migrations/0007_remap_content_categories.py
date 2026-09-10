from django.db import migrations


PROGRAM_MAP = {
    "flr": "development",
    "evangelism": "evangelism",
    "child_women": "social",
    "health": "social",
    "agriculture": "economic",
    "education": "development",
}

GALLERY_MAP = {
    "flr": "development",
    "community": "social",
    "education": "development",
    "health": "social",
    "leadership": "evangelism",
}


def remap_categories(apps, schema_editor):
    Program = apps.get_model("core", "Program")
    GalleryImage = apps.get_model("core", "GalleryImage")

    for old, new in PROGRAM_MAP.items():
        Program.objects.filter(category=old).update(category=new)

    for old, new in GALLERY_MAP.items():
        GalleryImage.objects.filter(category=old).update(category=new)

    Program.objects.exclude(category__in=["evangelism", "social", "economic", "development"]).update(
        category="evangelism"
    )
    GalleryImage.objects.exclude(category__in=["evangelism", "social", "economic", "development"]).update(
        category="evangelism"
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_update_content_categories"),
    ]

    operations = [
        migrations.RunPython(remap_categories, noop_reverse),
    ]
