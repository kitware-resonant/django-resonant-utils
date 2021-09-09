import warnings

from .db import *  # noqa: F401, F403

warnings.warn(
    'Imports from "girder_utils.models" should be renamed to use "girder_utils.db"',
    DeprecationWarning,
)
