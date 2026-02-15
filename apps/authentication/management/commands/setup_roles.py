from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Creates default groups and permissions for the different dashboards'

    def handle(self, *args, **options):
        # 1. Define Roles
        roles = ['Admin', 'Verifier', 'Uploader']

        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{role}" created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{role}" already exists'))

        # Future: Assign specific model permissions here
