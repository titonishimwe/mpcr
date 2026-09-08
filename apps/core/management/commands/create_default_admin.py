import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Creates a default superuser from environment variables if one does not exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
        email = os.getenv("DEFAULT_ADMIN_EMAIL", "info@mouvementpourchriste.org")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD", "MpcrRwanda2026!Secure")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists. Skipping."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' successfully created with email '{email}'."))
