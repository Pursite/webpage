from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# class SmallPagePagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 5


class StandardPagePagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

# class LargePagePagination(PageNumberPagination):
#     page_size = 9
#     page_size_query_param = 'page_size'
#     max_page_size = 10

# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
#
#
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'limit'
#     max_page_size = 100
#
#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'total_pages': self.page.paginator.num_pages,
#             'current_page': self.page.number,
#             'results': data
#         })
