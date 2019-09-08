#!/usr/bin/env python
import os
import sys
import django
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mileage_logger.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    django.setup()
    execute_from_command_line(sys.argv)
