from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='manager@m.com',
            first_name='Manager',
            last_name='Managerov',
            is_staff=True,
            is_superuser=False
        )

        user.set_password('123qwe456rty7')
        user.save()