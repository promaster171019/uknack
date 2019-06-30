from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


User = get_user_model()


class Command(BaseCommand):
    help = 'Set Password for every accounts'

    def handle(self, *args, **options):
        # print("Setting password for every accounts...")
        # password = 'wOlves22'
        # users = User.objects.all()
        # for user in users:
        #     user.set_password(password)
        #     user.save()
        #     print(user.email)
        print("Changing picture image url for every accounts...")
        users = User.objects.all()
        for user in users:
            print(user.picture)
            print(user.picture.url)
