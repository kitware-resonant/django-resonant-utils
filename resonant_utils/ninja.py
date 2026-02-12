from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ninja.security.http import HttpAuthBase
from oauth2_provider.oauth2_backends import get_oauthlib_core

if TYPE_CHECKING:
    from django.http import HttpRequest
    from oauth2_provider.models import AbstractAccessToken


# TODO: Remove this once https://github.com/django-oauth/django-oauth-toolkit/pull/1646 is released.
# Don't inherit from `HttpBearer`, since we have our own header extraction logic
class HttpOAuth2(HttpAuthBase):
    """Perform OAuth2 authentication, for use with Django Ninja."""

    openapi_scheme: str = "bearer"

    def __init__(self, *, scopes: list[str] | None = None) -> None:
        super().__init__()
        self.scopes = scopes if scopes is not None else []

    def __call__(self, request: HttpRequest) -> Any | None:
        oauthlib_core = get_oauthlib_core()
        # This also sets `request.user`,
        # which Ninja does not: https://github.com/vitalik/django-ninja/issues/76
        valid, r = oauthlib_core.verify_request(request, scopes=self.scopes)

        if not valid:
            return None

        return self.authenticate(request, r.access_token)

    def authenticate(self, request: HttpRequest, access_token: AbstractAccessToken) -> Any | None:
        """
        Determine whether authentication succeeds.

        If this returns a truthy value, authentication will succeed.
        Django Ninja will set the return value as `request.auth`.

        Subclasses may override this to implement additional authorization logic.
        """
        return access_token
