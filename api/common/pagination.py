from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    
    page_size = 20
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        """
        重写返回数据
        """
        response = super().get_paginated_response(data)
        response.data['current'] = self.page.number
        return response


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    
    default_limit = 10