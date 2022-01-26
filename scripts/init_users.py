#!/usr/bin/env python
def main() -> None:
    from django.contrib.auth.models import User

    User.objects.all().delete()
    User.objects.create_superuser(
        username="admin", email="admin@example.com", password="secret"
    )
    print("Initialized admin user!")


if __name__ == "__main__":
    import os
    from pathlib import Path
    import sys

    import django

    sys.path.append(str(Path(__file__).parents[1]))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()
    main()
