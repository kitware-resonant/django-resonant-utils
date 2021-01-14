from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class BoundedLimitOffsetPagination(LimitOffsetPagination):
    """
    Pagination class that forces pagination with an upper bound.

    DRF's built-in paginators such as LimitOffsetPagination will cause
    your endpoints to return different structure based on whether or not
    paging parameters were passed in the request. In most cases it's desirable
    to force pagination on endpoints that could return large result sets.
    Using this class has three benefits:

    1. It will always return responses in their paged structure, i.e. a
       JSON Object with "count", and a "results" Array. This is achieved by
       providing a default limit that is used if none is passed.
    2. It enforces a reasonable upper bound on page sizes. Without this, users could
       circumvent the intent of pagination by simply providing a high enough limit.
    3. It adds the Link header to the response, making it easier for clients to
       navigate through pages of results.

    The default limit will be the value of DRF's normal PAGE_SIZE setting, or
    the max limit if that is not set or falsy. The upper bound on the limit is 1000.
    """

    max_limit = 1000

    def get_limit(self, request) -> int:
        return super().get_limit(request) or self.max_limit

    def get_paginated_response(self, data) -> Response:
        response = super().get_paginated_response(data)

        # Add links, per https://tools.ietf.org/html/rfc8288
        links = [
            # (relation_type, target)
            ('prev', self.get_previous_link()),
            ('next', self.get_next_link()),
        ]
        # Always set a Link header, even if it's empty
        response['Link'] = ', '.join(
            f'<{target}>; rel="{relation_type}"'
            for relation_type, target in links
            if target is not None
        )

        return response
