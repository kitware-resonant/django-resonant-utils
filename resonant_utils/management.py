import os
import sys

from django.core.management import ManagementUtility
from django.core.management.color import color_style


def execute_from_command_line(argv: list[str] | None = None) -> None:
    """Behave like `django.core.management.execute_from_command_line`, but print settings errors."""
    utility = ManagementUtility(argv)
    try:
        utility.execute()
    finally:
        if utility.settings_exception is not None and "DJANGO_AUTO_COMPLETE" not in os.environ:
            # A settings exception may exist after least 4 different code paths:
            # * Clean return from successfully printing help, which will have already printed the
            #   settings error, but we'll accept a second print here, for a simpler implementation.
            # * Clean return from running any other command
            # * `sys.exit(1)` if a command cannot be found (possibly because it's from an app,
            #   which aren't loaded if settings fail)
            # * `sys.exit(0)`, if autocomplete was invoked; we won't print here, to avoid spam (but
            #   we should still detect autocomplete natively, not hardcoding around `sys.exit(0)`)
            style = color_style()
            sys.stderr.write(
                style.NOTICE(
                    "Note that settings are not properly configured "
                    f"(error: {utility.settings_exception}).\n"
                )
            )
