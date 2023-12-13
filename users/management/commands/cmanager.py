from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='manager@mail.кг',
            first_name='manager',
            last_name='manager',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('manager')
        group = Group.objects.get(name='Менеджер')
        group.user_set.add(user)
        user.save()
