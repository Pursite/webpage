from rest_framework.pagination import PageNumberPagination, CursorPagination


class SmallPagePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class StandardPagePagination(CursorPagination):
    page_size = 4
    ordering = '-created_time'


class LargePagePagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 10