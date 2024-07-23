from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@diplom.com',
            last_name='Admin',
            first_name='Admin',
            birthday='1995-01-01',
            phone='89876543210',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123qweasd')
        user.save()
