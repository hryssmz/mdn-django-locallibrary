# main.py
import sys

from django.conf import settings

if __name__ == "__main__":
    import django

    sys.path.append(".")

    from app.settings import DATABASES, DEBUG, INSTALLED_APPS

    settings.configure(
        DATABASES=DATABASES, DEBUG=DEBUG, INSTALLED_APPS=INSTALLED_APPS
    )
    django.setup()

    from django.contrib.auth.models import User

    User.objects.all().delete()
    User.objects.create_superuser(
        username="admin", email="admin@example.com", password="secret"
    )
