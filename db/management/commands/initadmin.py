from django.conf import settings
from django.core.management.base import BaseCommand

from db.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                admin = User.objects.create_superuser(**user)
                admin.is_active = True
                admin.is_admin = True
                admin.is_staff = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
