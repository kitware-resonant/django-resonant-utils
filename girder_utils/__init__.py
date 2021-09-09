from importlib.metadata import PackageNotFoundError, version

import django

try:
    __version__ = version('django-girder-utils')
except PackageNotFoundError:
    # package is not installed
    pass

if django.VERSION < (3, 2):
    default_app_config = 'girder_utils.apps.GirderUtilsConfig'
