from rest_framework.pagination import LimitOffsetPagination


class BoundedLimitOffsetPagination(LimitOffsetPagination):
    """
    Pagination class that forces pagination with an upper bound.

    DRF's built-in paginators such as LimitOffsetPagination will cause
    your endpoints to return different structure based on whether or not
    paging parameters were passed in the request. In most cases it's desirable
    to force pagination on endpoints that could return large result sets.
    Using this class has two benefits:

    1. It will always return responses in their paged structure, i.e. a
       JSON Object with "count", and a "results" Array. This is achieved by
       providing a default limit that is used if none is passed.
    2. It enforces a reasonable upper bound on page sizes. Without this, users could
       circumvent the intent of pagination by simply providing a high enough limit.

    The default limit will be the value of DRF's normal PAGE_SIZE setting, or
    the max limit if that is not set or falsy. The upper bound on the limit is 1000.
    """

    max_limit = 1000

    def get_limit(self, request) -> int:
        return super().get_limit(request) or self.max_limit
