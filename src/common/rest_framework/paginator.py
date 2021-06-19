from rest_framework import pagination
from rest_framework.views import Response


class CustomAPIPagination(pagination.PageNumberPagination):
    page_size = 50

    def get_next_pageitem(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        next_page = {"param": "?" + self.page_query_param + "=", "next": page_number}
        return next_page

    def get_previous_pageitem(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        previous_page = {"param": "?" + self.page_query_param + "=", "previous": page_number}
        return previous_page

    def get_page_context_to_json(self):
        page = {
            "current_page": self.page.number,
            "num_pages": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "next": self.get_next_pageitem(),
            "previous": self.get_previous_pageitem(),
            "query_param": "?" + self.page_query_param + "=",
        }
        return page

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.get_page_context_to_json(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class CustomAPIPaginationWithNoLimit(pagination.PageNumberPagination):
    page_size = 500

    def get_next_pageitem(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        next_page = {"param": "?" + self.page_query_param + "=", "next": page_number}
        return next_page

    def get_previous_pageitem(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        previous_page = {"param": "?" + self.page_query_param + "=", "previous": page_number}
        return previous_page

    def get_page_context_to_json(self):
        page = {
            "current_page": self.page.number,
            "num_pages": self.page.paginator.num_pages,
            "count": self.page.paginator.count,
            "next": self.get_next_pageitem(),
            "previous": self.get_previous_pageitem(),
            "query_param": "?" + self.page_query_param + "=",
        }
        return page

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.get_page_context_to_json(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )
