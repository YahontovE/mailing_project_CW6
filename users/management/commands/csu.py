from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='yahontov@inbox.ru',
            first_name='John',
            last_name='Yahontov',
            is_superuser=True,
            is_staff=True,

        )
        user.set_password('123qwe456rty')
        user.save()
