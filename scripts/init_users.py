#!/usr/bin/env python
def main() -> None:
    from django.contrib.auth.models import Group, User

    User.objects.all().delete()

    # Create an admin user.
    User.objects.create_superuser(
        username="admin", email="admin@example.com", password="secret"
    )
    print("Initialized admin user!")

    # Create a new group.
    Group.objects.create(name="Library Members")

    # Create a library member user.
    User.objects.create_user(
        username="john", email="john@example.com", password="secret"
    )
    User.objects.get(username="john").groups.add(
        Group.objects.get(name="Library Members")
    )


if __name__ == "__main__":
    import os
    from pathlib import Path
    import sys

    import django

    sys.path.append(str(Path(__file__).parents[1]))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    django.setup()
    main()
