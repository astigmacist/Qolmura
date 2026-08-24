import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Idempotent: creates (or resets the password of) a default superuser so
    /admin/ has a working login without an interactive createsuperuser prompt.

    Override the defaults with QOLMURA_ADMIN_USERNAME / QOLMURA_ADMIN_EMAIL /
    QOLMURA_ADMIN_PASSWORD env vars before running in anything but local dev.
    """

    help = "Ensure a default Qolmura admin superuser exists."

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-if-unconfigured",
            action="store_true",
            help="Exit successfully when QOLMURA_ADMIN_PASSWORD is not configured.",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("QOLMURA_ADMIN_USERNAME", "admin")
        email = os.getenv("QOLMURA_ADMIN_EMAIL", "admin@qolmura.kz")
        password = os.getenv("QOLMURA_ADMIN_PASSWORD")
        if not password:
            if options["skip_if_unconfigured"]:
                self.stdout.write(self.style.WARNING("Admin creation skipped: QOLMURA_ADMIN_PASSWORD is not configured."))
                return
            raise CommandError("Set QOLMURA_ADMIN_PASSWORD before creating the Qolmura administrator.")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        if not created:
            user.is_staff = True
            user.is_superuser = True
            user.email = email
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} superuser '{username}'. Log in at /admin/."))
