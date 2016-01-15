from rest_framework.pagination import PageNumberPagination

__author__ = 'Emilio-Emilio'


class BasePagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    page_query_param = 'page'