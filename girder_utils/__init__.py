from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('django-girder-utils')
except PackageNotFoundError:
    # package is not installed
    pass
