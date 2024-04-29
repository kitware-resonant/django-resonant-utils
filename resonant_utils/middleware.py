from __future__ import annotations

from django.http.response import HttpResponseRedirectBase
from django.middleware.common import CommonMiddleware


class HttpResponsePermanentRedirect(HttpResponseRedirectBase):
    status_code = 308


class PermanentRedirectCommonMiddleware(CommonMiddleware):
    response_redirect_class = HttpResponsePermanentRedirect
