from django.db import migrations, models


def seed_team(apps, schema_editor):
    TeamMember = apps.get_model("core", "TeamMember")
    TeamMember.objects.get_or_create(
        name="Eraste NDAYISENGA",
        defaults={
            "position": "Legal Representative",
            "phone": "(+250) 788 812 075",
            "email": "info@mouvementpourchriste.org",
            "order": 1,
            "is_active": True,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("position", models.CharField(max_length=200)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Team Member",
                "verbose_name_plural": "Team Members",
                "ordering": ["order", "name"],
            },
        ),
        migrations.RunPython(seed_team, migrations.RunPython.noop),
    ]
