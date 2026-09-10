from django.core.management.base import BaseCommand

from apps.core.models import ensure_cms_defaults


class Command(BaseCommand):
    help = "Seed editable website content defaults for site settings, pages, and hero slides"

    def handle(self, *args, **options):
        ensure_cms_defaults()
        self.stdout.write(self.style.SUCCESS("Website content defaults are ready."))
