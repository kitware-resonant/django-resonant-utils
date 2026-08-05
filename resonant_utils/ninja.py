from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast
from unittest.mock import Mock

from django.http import HttpRequest, QueryDict
from ninja.security.http import HttpAuthBase
from ninja.testing import TestClient as UpstreamTestClient
from oauth2_provider.oauth2_backends import get_oauthlib_core

if TYPE_CHECKING:
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


# TODO: Remove once https://github.com/vitalik/django-ninja/pull/1680 is released.
# ruff: disable[C901,PLR0912,SLF001]
class TestClient(UpstreamTestClient):
    def _build_request(  # type: ignore[override]
        self,
        method: str,
        path: str,
        data: dict,  # type: ignore[type-arg]
        request_params: dict[str, Any],
    ) -> HttpRequest:
        request = HttpRequest()
        request.method = method
        body = request_params.pop("body", b"")
        request._body = body.encode() if isinstance(body, str) else body
        # Django CsrfViewMiddleware respects "_dont_enforce_csrf_checks" on a Request
        request._dont_enforce_csrf_checks = True  # type: ignore[attr-defined]

        request.auth = None  # type: ignore[attr-defined]
        if "user" not in request_params:
            request.user = Mock()
            request.user.is_authenticated = False
            request.user.is_staff = False
            request.user.is_superuser = False

        files = request_params.pop("FILES", None)
        if files is not None:
            request.FILES = files

        # django-stubs types "request.GET"/"request.POST" as immutable, which holds for a
        # fully-constructed request but not for one from "HttpRequest.__init__"
        if isinstance(data, QueryDict):
            request.POST = data  # type: ignore[assignment]
        elif isinstance(data, (str, bytes)):
            request._body = data.encode() if isinstance(data, str) else data
        elif data:
            # Cast to the mutable base type, so mutating methods resolve to the base-class ones
            # returning "None"; the immutable overrides return "NoReturn", which would make mypy
            # consider every following statement unreachable and silently skip type checking it.
            post = cast("QueryDict", request.POST)
            for k, v in data.items():
                post[k] = v

        query_string = ""
        query_params = request_params.pop("query_params", None)
        if "?" in path:
            # Store "query_string" verbatim here, for assignment to "request.META.QUERY_STRING",
            # to ensure empty parameter syntax is preserved
            path, query_string = path.split("?", maxsplit=1)
            request.GET = QueryDict(query_string)
        elif query_params is not None:
            # Cast for the same reason as "request.POST" above
            get = cast("QueryDict", request.GET)
            for k, v in query_params.items():
                if isinstance(v, list):
                    for item in v:
                        get.appendlist(k, item)
                else:
                    get[k] = v
            query_string = request.GET.urlencode()
        request.path = path
        # If "settings.FORCE_SCRIPT_NAME" is set, "request.path_info" ought
        # to respect it, but this class skips the Django URL resolver,
        # so don't bother
        request.path_info = path

        request.META = request_params.pop(
            "META",
            {
                "REQUEST_METHOD": request.method,
                "SCRIPT_NAME": "",
                "PATH_INFO": request.path_info,
                "QUERY_STRING": query_string,
                "SERVER_NAME": "testserver",
                "SERVER_PORT": "80",
                "SERVER_PROTOCOL": "HTTP/1.1",
                "REMOTE_ADDR": "127.0.0.1",
            },
        )
        request.META.update(
            {
                f"HTTP_{k.replace('-', '_').upper()}": v
                for k, v in request_params.pop("headers", {}).items()
            }
        )

        for k, v in request_params.items():
            setattr(request, k, v)
        return request


# ruff: enable[C901,PLR0912,SLF001]
