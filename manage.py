#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thedmstoolkit.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    is_testing = "test" in sys.argv
    if is_testing:
        import coverage  # type: ignore

        cov = coverage.coverage(
            source=["toolkit/views"], omit=["*/tests/*", "*/Tests/*"]
        )
        cov.set_option("report:show_missing", True)
        cov.erase()
        cov.start()

    execute_from_command_line(sys.argv)

    if is_testing:
        cov.stop()
        cov.save()
        cov.xml_report()
        cov.report()


if __name__ == "__main__":
    main()
